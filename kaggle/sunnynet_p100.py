"""SunnyNet on Kaggle: one big English training run with milestone sampling.

Usage:
  1. Kaggle -> New Notebook (Python), set accelerator = GPU P100 16GB (or V100/T4 16GB).
  2. Paste this file into the notebook (each section is one cell-compatible block,
     or just run it as a whole script).
  3. GPU free tier: 30h/week, 9h/day - the training run below fits in one session.

What it does:
  clone repo -> patch train.py (--save-every milestone checkpoints)
  -> collect corpus (curated EN classics + Python code) -> build BPE tokens
  -> smoke test (60 steps, CUDA) -> probe batch size -> train p100m
  -> sample milestones so you can watch prose become coherent.

Everything is plain torch - no prebuilt C kernel, no pip install on GPU.
"""

from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path

# ============================== CONFIG ======================================
REPO_URL = "https://github.com/SunnyClaw-cx/SunnyNet"  # edit to your fork if needed
REPO_DIR = "/kaggle/working/SunnyNet"

PRESET = "p100m"  # ~94M compute-stack params (report's main preset)
STEPS = 24_000  # ~98M tokens at batch 8 ~= 0.96 tokens/param, ~7h on a P100 (9h cap, no resume)
BATCH_CANDIDATES = (8, 4, 2)  # probe from largest down until forward+backward fits
SEQ_LEN = 512
MIX = "en_literature=1.0"  # stage 1 = coherent English prose
SAVE_EVERY = 2_000  # milestone checkpoints every N steps (12 + final)
VAL_EVERY = 500  # 48 val checks total - keeps the run fast
NO_EARLY_STOP = True

VOCAB = 8192
PRESET_DIMS = {  # mirrors _preset_cfg in train/train.py (p100m/p100mw have no static cfg method)
    "p100m": {"dim": 1024, "inner": 1792, "rank": 640, "layers": 14, "h_max": 16384.0},
    "p100mw": {"dim": 1408, "inner": 1920, "rank": 1024, "layers": 8, "h_max": 16384.0},
    "proto20m": {"dim": 512, "inner": 896, "rank": 320, "layers": 10, "h_max": 8192.0},
}
# 22 extra curated classics (verified via Gutenberg search; deduped against the
# repo's built-in EXTRA_EN_BOOKS, which adds 13 more public-domain EN titles).
EXTRA_BOOKS = [
    15,
    2852,
    7700,
    19640,
    7100,
    19797,
    1260,
    1400,
    18581,
    35,
    1399,
    829,
    521,
    33,
    599,
    1184,
    135,
    3707,
    4300,
    2781,
    768,
    145,
]

SAMPLE_PROMPTS = [
    "It was the best of times, ",
    "Once upon a time, ",
    "The morning sun was ",
]
# Where results land: /kaggle/output on Kaggle (pullable via `kaggle kernels pull`),
# a local dir when run on your machine.
OUT_DIR = Path("/kaggle/output") if Path("/kaggle").exists() else Path("kaggle_out")
# ==============================================================================


def sh(cmd: list[str], cwd: str | None = None, timeout: int = 3600) -> None:
    print(f"$ {' '.join(cmd)}")
    r = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False
    )
    if r.stdout.strip():
        print(r.stdout[-4000:])
    if r.returncode != 0:
        sys.exit(f"FAILED: {' '.join(cmd)}\n{r.stderr[-4000:]}")


def run_capture(
    cmd: list[str], cwd: str | None = None, timeout: int = 3600
) -> tuple[int, str, str]:
    """Like sh() but never exits - sampling must not kill the run."""
    print(f"$ {' '.join(cmd)}")
    r = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False
    )
    print(r.stdout[-3000:])
    return r.returncode, r.stdout, r.stderr


def main() -> None:
    # ---- 1. clone ------------------------------------------------------------
    print("== [1/6] clone ==")
    if not Path(REPO_DIR).exists():
        sh(["git", "clone", "--depth", "1", REPO_URL, REPO_DIR])

    # ---- 2. patch train.py: --save-every milestone checkpoints ---------------
    print("== [2/6] patch ==")
    train = Path(REPO_DIR, "train", "train.py")
    src = train.read_text(encoding="utf-8")
    if '"--save-every"' in src:
        print("  already patched, skipping")
    else:
        arg_marker = 'ap.add_argument("--save-ckpt", type=str, default="")'
        hist_marker = 'log["history"].append(rec)'
        assert src.count(arg_marker) == 1, (
            "arg_marker not unique/missing - upstream drifted?"
        )
        assert src.count(hist_marker) == 1, (
            "hist_marker not unique/missing - upstream drifted?"
        )
        src = src.replace(
            arg_marker,
            arg_marker + '\n    ap.add_argument("--save-every", type=int, default=0,\n'
            '                    help="里程碑 checkpoint 间隔步数 (0=关闭)")',
        )
        milestone_block = textwrap.dedent("""
            if args.save_every > 0 and args.save_ckpt and (step + 1) % args.save_every == 0:
                sp = Path(args.save_ckpt).with_name(
                    Path(args.save_ckpt).stem + f"_{step+1:06d}" + Path(args.save_ckpt).suffix)
                sp.parent.mkdir(parents=True, exist_ok=True)
                sd2 = {k: v.detach().cpu() for k, v in model.state_dict().items()}
                torch.save({"arch": args.arch, "model": sd2,
                            "config": cfg.__dict__ if hasattr(cfg, "__dict__") else cfg,
                            "summary": {"step": step + 1, "val_loss": rec["val_loss"]}}, sp)
                print(f"    里程碑 checkpoint -> {sp}")
        """).rstrip("\n")
        ind = " " * 12  # matches 'log["history"].append(rec)' indentation
        src = src.replace(
            hist_marker,
            hist_marker
            + "\n"
            + "\n".join(ind + ln for ln in milestone_block.split("\n")),
        )
        train.write_text(src, encoding="utf-8")
        print("  patched train.py (+save-every)")

    # ---- 3. corpus: curated EN classics + Python code -------------------------
    print("== [3/6] corpus ==")
    sh([sys.executable, "prepare_data.py", "--only-code"], cwd=REPO_DIR)
    sh(
        [
            sys.executable,
            "-c",
            f"import prepare_data as pd; s,c=pd.collect_books({EXTRA_BOOKS}, 8); print(s); print(c)",
        ],
        cwd=REPO_DIR,
    )
    sh([sys.executable, "build_corpus.py", "--vocab-size", str(VOCAB)], cwd=REPO_DIR)

    # ---- 4. smoke test: 60 steps on the real model, catch OOM/NaN early ------
    print("== [4/6] smoke ==")
    sh(
        [
            sys.executable,
            "train/train.py",
            "--arch",
            "sunnynet",
            "--preset",
            PRESET,
            "--device",
            "cuda",
            "--threads",
            "1",
            "--steps",
            "60",
            "--batch-size",
            str(BATCH_CANDIDATES[-1]),
            "--seq-len",
            str(SEQ_LEN),
            "--mix",
            MIX,
            "--val-every",
            str(STEPS // 3),
        ],
        cwd=REPO_DIR,
    )

    # ---- 5. probe batch size, then train --------------------------------------
    print("== [5/6] train ==")
    bs = probe_batch()
    print(f"  batch={bs} selected")
    cmd = [
        sys.executable,
        "train/train.py",
        "--arch",
        "sunnynet",
        "--preset",
        PRESET,
        "--device",
        "cuda",
        "--threads",
        "1",
        "--steps",
        str(STEPS),
        "--batch-size",
        str(bs),
        "--seq-len",
        str(SEQ_LEN),
        "--mix",
        MIX,
        "--val-every",
        str(VAL_EVERY),
        "--save-every",
        str(SAVE_EVERY),
        "--save-ckpt",
        f"runs/{PRESET}_en.pt",
    ]
    if NO_EARLY_STOP:
        cmd.append("--no-early-stop")
    sh(cmd, cwd=REPO_DIR, timeout=32400)  # a full training run can exceed the default

    # ---- 6. sample milestones: watch the text come together ------------------
    print("== [6/6] milestone samples ==")
    sample_milestones()
    write_results()


def probe_batch() -> int:
    """Largest batch whose forward+backward fits in VRAM (O(N) model, no KV cache)."""
    script = textwrap.dedent(f"""
        import sys; sys.path.insert(0, '.')
        import torch
        from sunnynet.model import SunnyConfig, SunnyNet
        _d = {PRESET_DIMS[PRESET]}
        c = SunnyConfig(vocab_size={VOCAB}, **_d)
        m = SunnyNet(c).cuda(); opt = torch.optim.AdamW(m.parameters())
        for bs in {BATCH_CANDIDATES}:
            x = torch.randint(0, {VOCAB}, (bs, {SEQ_LEN}), device='cuda')
            y = x.roll(-1, 1)
            try:
                opt.zero_grad()
                torch.nn.functional.cross_entropy(m(x).reshape(-1, {VOCAB}), y.reshape(-1)).backward()
                torch.cuda.synchronize()
                print(f"bs={{bs}} OK: {{torch.cuda.max_memory_reserved()/1e6:.0f}}MB reserved")
                print("PICKED " + str(bs)); sys.exit(0)
            except torch.cuda.OutOfMemoryError:
                print(f"bs={{bs}} OOM"); torch.cuda.empty_cache()
        sys.exit(1)
    """)
    r = subprocess.run(
        [sys.executable, "-c", script],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    for ln in r.stdout.splitlines():
        if ln.startswith("PICKED "):
            return int(ln.split()[1])
    sys.exit(f"batch probe failed:\n{r.stdout}\n{r.stderr}")


def sample_milestones() -> None:
    """Generate from each milestone checkpoint; store samples for write_results()."""
    cks = [
        p for p in sorted(Path(REPO_DIR, "runs").glob(f"{PRESET}_en*.pt")) if p.exists()
    ]
    sample_milestones.samples = {}
    sample_milestones.keep = []
    if not cks:
        print("no checkpoints found - training failed, nothing to sample")
        return
    # sample up to 3 (first / middle / last) to keep output small
    if len(cks) >= 3:
        picks = {cks[0], cks[len(cks) // 2], cks[-1]}
    else:
        picks = set(cks)
    sample_milestones.keep = sorted(picks)
    for ck in sorted(picks):
        print(f"\n### {ck.name}")
        outs = {}
        for p in SAMPLE_PROMPTS:
            _, out, err = run_capture(
                [
                    sys.executable,
                    "-m",
                    "sunnynet.cli",
                    "--ckpt",
                    str(ck),
                    "--prompt",
                    p,
                    "--max-new",
                    "60",
                    "--temperature",
                    "0.7",
                ],
                cwd=REPO_DIR,
            )
            outs[p] = out[-900:] if out.strip() else f"(empty) {err.strip()[-200:]}"
        sample_milestones.samples[ck.name] = outs


def write_results() -> None:
    """Copy sampled checkpoints + samples + val history to OUT_DIR (pullable)."""
    import shutil

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for ck in list(getattr(sample_milestones, "keep", [])) + [
        Path(REPO_DIR, f"runs/{PRESET}_en.pt")
    ]:
        if ck.exists():
            shutil.copy(ck, OUT_DIR / ck.name)
    res = {"samples": getattr(sample_milestones, "samples", {}), "val_history": []}
    log = Path(REPO_DIR, f"runs/{PRESET}_en.json")
    if log.exists():
        hist = json.loads(log.read_text(encoding="utf-8")).get("history", [])
        step = max(1, len(hist) // 60)
        res["val_history"] = hist[::step]
    (OUT_DIR / "results.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nresults -> {OUT_DIR} (results.json + checkpoint copies)")


if __name__ == "__main__":
    main()
