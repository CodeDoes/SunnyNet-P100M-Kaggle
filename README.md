# SunnyNet p100m English Kaggle run

This repository contains the trained checkpoint, its matching BPE tokenizer, and the Kaggle script and metadata used for the run. The checkpoint has 102,126,662 parameters and was trained for 24,000 steps on English prose. Validation loss was **2.475938** (perplexity **11.8929**). Generated text is still grammatically weak; this is a text-completion model, not an instruction-following chatbot.

The 442,190,099-byte checkpoint is stored with Git LFS. After cloning, run `git lfs pull` if `models/p100m_en.pt` is only a pointer. SHA-256: `cde00ce3309a21f6f5b5e9666727bb467e50d37d6e80c2bab3b5e2c977fdce38`.

## Try a prompt

Clone [SunnyNet](https://github.com/SunnyClaw-cx/SunnyNet) next to this repository, install its Python dependencies (`python -m pip install -e .` from the SunnyNet directory), then run from the SunnyNet directory:

```sh
python -m sunnynet.cli --ckpt ../SunnyNet-P100M-Kaggle/models/p100m_en.pt --tokenizer ../SunnyNet-P100M-Kaggle/models/p100m_en_tokenizer.json --prompt "Once upon a time, " --max-new 40 --temperature 0.7 --top-k 40 --seed 42 --threads 1
```

Change `--prompt` to test other completions. The tokenizer included here is required: the tokenizer in a different SunnyNet checkout can encode prompts differently.

## Observed input and output

These are actual generated continuations, not selected excerpts. Each example used the command above, changing only `--prompt`. Output below excludes the prompt itself; trailing spaces are trimmed for display.

**Input:** `Once upon a time, `

```text
and was horning to the days in the
hand who had take the place of the
```

**Input:** `The morning sun was `

```text
a little to do of the scape of the
turb which clear the bark
```

**Input:** `It was the best of times, `

```text
and was scornce like the scape of the
visic of the place, of
```

The Kaggle submission files are `kaggle/sunnynet_p100.py` and `kaggle/kernel-metadata.json`. No Kaggle API keys are stored in this repository.
