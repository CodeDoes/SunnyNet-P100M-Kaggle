# Real p100m prompt completions

These are 40 unfiltered, locally generated continuations from `models/p100m_en.pt` with `models/p100m_en_tokenizer.json`. The checkpoint SHA-256 is `cde00ce3309a21f6f5b5e9666727bb467e50d37d6e80c2bab3b5e2c977fdce38`.

Generation used CPU PyTorch, `--max-new 128 --temperature 0.7 --top-k 40 --top-p 0.95 --seed 42 --threads 1`, resetting the seed for each prompt. Each output excludes its input; only trailing whitespace was trimmed for display. Repetitions and malformed words are left as generated. From a SunnyNet checkout next to this repository, replace `PROMPT` in:

```sh
python -m sunnynet.cli --ckpt ../SunnyNet-P100M-Kaggle/models/p100m_en.pt --tokenizer ../SunnyNet-P100M-Kaggle/models/p100m_en_tokenizer.json --prompt "PROMPT" --max-new 128 --temperature 0.7 --top-k 40 --top-p 0.95 --seed 42 --threads 1
```

## 01 Input: 'Once upon a time, '

```text
and was horning to the days in the
hand who had take the place of the recess was suppose of the grass the
farter of his face, and which was the latch drifive to find the mounted
to be the same of the room of the rooms of
```

## 02 Input: 'The morning sun was '

```text
a little to do of the scape of the
turb which clear the bark of the barefize of the instead of the women of the
wite was the first in the eyes of the rooms of there the wilder and
standing passed the small of
```

## 03 Input: 'It was the best of times, '

```text
and was scornce like the scape of the
visic of the place, of the eyes of the husband of the eyes which I had
delighted the great the latter of the first seen. The these was complained and
standing passed the small of
```

## 04 Input: 'She opened the door and '

```text
suref a scholl. She had also
so contract to the words of the day. We she should be a strief. And then in the
most care of it. But it had returned the mounted to be the same of the
room of the Bropley
```

## 05 Input: 'The old house stood '

```text
ne with the carching of the scape of the
visic of the place, of the eyes and the ship in the balebour and had in the
most care of it. But it had returned the mounted to be the same of the
room of the Bropley
```

## 06 Input: 'He looked at her and said, '

```text
“
“I must have been to Mr. But I think in a surprise of the day. In this
work of a strief. It is in the most care of it. I don’t know my refusion I
have been the determined in passion of the bi
```

## 07 Input: 'In the quiet of the evening, '

```text
and with the carching of the scape of the
visic of the place, of the eyes of the husband of the eyes which I had
delighted the great the latter of the first seen. The these was complained and
standing passed the small of
```

## 08 Input: 'The letter began, '

```text
anding free to the puillion
in the hand. They well to get his own and don't the
husband of the hideful found in the moon. He had a little words
was coming to the blue with the determinatory passion and think
```

## 09 Input: 'They rode through the forest '

```text
of of hours were she had scape
fresh and been on a sort of eyes. We she should be a strief fare in a man of
secretched, but he did not return with a handsome he said.
“You not know that any shuder he
```

## 10 Input: 'I had never seen '

```text
to you to look him.
“That is not not a disposition a you really of every eye.
I have been you will be women a little pleasure which you have one work for me?
The half to be much a little passion is think
```

## 11 Input: 'At the edge of the sea, '

```text
and was she knew of the scape of the
visic of the place, of the eyes of the husband of the eyes which I had
delighted the great the latter of the first seen. The these was complained and
standing passed the small of
```

## 12 Input: 'The stranger whispered, '

```text
and was she knew of
the scape of the table. The calmbour back of the sort of the great of the eyes which
Therein the most care of it. But it had returned the mounted to be
the same in the room of the Bropley
```

## 13 Input: 'It was a cold night, '

```text
and was horning to the days in black when he had
beneed his occasion. We she should be a strief fare in his face, and
to say, but he did not return with a handsome he said.
“You not know that any shuder he
```

## 14 Input: 'The city was asleep when '

```text
hes a little light of silking
face which and been on a sort of eyes. We she should be a strief
fare in a man offer, and that it had been word to find in the hand
to be much a little passion is think
```

## 15 Input: 'Beyond the hills, '

```text
and was hardly part of
the scape of the visic of the place, of the eyes of the
husband of the eyes which I had delighted the resolent, but the drifive of
“What is the door, you cannot me, and they are a more
```

## 16 Input: 'The captain turned and '

```text
suref a smoke of the scape of the
visic of the place, of the eyes of the husband of the eyes which I had
delighted the great the latter of the first seen. The these was complained and
standing passed the small of
```

## 17 Input: 'My dear friend, '

```text
and with the carching of the scape of the
visic of the place, of the eyes of the husband of the eye which I had
delighted the great the latter of the first seen. The these was complained and
standing passed the small of
```

## 18 Input: 'She could not remember '

```text
that with a carriage of the scape of which
the dress of the business and drinking at the window of the
far-four in the moon was the first in the eyes of the rooms of there the
wilder and standing passed the small of
```

## 19 Input: 'The rain fell on '

```text
the long of the soft of girls were not
discust to the other part of the sort of the great of the eyes which I had
delighted the great the latch drifive of the rooms of there the wilder and
standing passed the small of
```

## 20 Input: 'A long time ago, '

```text
and was horror is the day scape or not a day of more
in a moment of his bristom-grees of the eyes which I had delighted the great
which he had expened her monst. The here was complained and standing passed the small
d
```

## 21 Input: 'The garden gate creaked as '

```text
suref a school. There was bore than he had
beneed his occasion. We she should be a strief. And then in the most
care of it. But it with her fond small there were waiting and
standing passed the small d
```

## 22 Input: 'It is a truth universally acknowledged, '

```text
and with
a carriage of the scape of the trave and clease of her eyes. We she
should not a strief fare in a man offer, and that it had been word to find in the hand
to be much a little passion is think
```

## 23 Input: 'The child ran toward '

```text
the with hour to do of the scape of the
visic of the place, of the eyes and the ship in the baleb which I had
delighted the great the latter of the first seen. The these was complained and
standing passed the small of
```

## 24 Input: 'In the middle of the night, '

```text
and was horning to the place in
the hands and been on a sort of eyes. We she should be a strief
fare in a man offer, and that it was done words was coming to the blue
with the deters of the world shuding on
```

## 25 Input: 'He took the book from the shelf and '

```text
slowly
hour to do of the scape of the table. The calmbour back of the sort of
the great of the hide which I had delighted the great the
lines of word to the rooms of there the wilder and standing passed the small
d
```

## 26 Input: 'Across the river there was '

```text
sure to the child.
“That is not not a disposition a you of better and speak.
What has no runned with the both of its at the other, but he did
not return to speak the work the deters of the world and there was
```

## 27 Input: 'When I returned home, '

```text
and was a carriage of the scape of the
visic of the place, of the eyes and the ship in the balebour and had in the
most care of it. But I had returned the mounted to be the same of the
room of the Bropley
```

## 28 Input: 'They gathered around the fire and '

```text
slowly
hour to do of the scape of the table. The calm of back of the sort of
the great of the hide which I had delighted the great the
lines of word to the rooms of there the wilder and standing passed the small
d
```

## 29 Input: 'No one had expected '

```text
to the hour to do of the scape of the
visible of the place, of the eyes of the husband of the eyes which I had
delighted the great the latter of the first seen. The these was complained and
standing passed the small of
```

## 30 Input: 'The woman in the red coat '

```text
and with the carching of the scape of the
visic of the place, of the eyes and the ship in the balebour and had in the
most care of it. But it had returned the mounted to be the same of the
room of the Bropley
```

## 31 Input: 'The stars were bright above '

```text
him with the carching of the scape of the
visic of the place, of the eyes of the husband of the eyes which I had
delighted the great the latter of the first seen. The these was complained and
standing passed the small of
```

## 32 Input: 'The traveler found a letter '

```text
s of hour to do of the scape of the
visible of the place, of the eyes and the hide in the baleb which I had
decled the great the latter of the fret of the mouth of the wild, and
standing passed the small of
```

## 33 Input: 'I remember the first time '

```text
tol found into the poor
shout in the hand. They were on my face, and would every eye
of the window showed with the composy of the great which
Hesterd words was coming to the blue of the determinator
was so long than he
```

## 34 Input: 'On the other side of the door '

```text
of off the school. There was bore than he had
beneed his occasion. We had alreaded in the baleb of the commony
of the old which the strid words of the fross of the day of my feeling in the mixting which
bre
```

## 35 Input: 'He promised that he would '

```text
never
free to do of the scape of the whole. The calm of back of the sort of
the great of the eyes which I had delighted the great the latch drifive of the
plank of the day of my feeling in the mixting than d
```

## 36 Input: 'It was only after sunset that '

```text
this time of the door.
“That is not not a disposition my father, before every eye.
I have been you will be women a little pleasure which I be extracted to me, as I thought
I cannot be a grust any life; I
```

## 37 Input: 'The village had been quiet for '

```text
the long of the
lighting of girls were not been than sympa of the day. We she should be
dead out of the surprise. “Well, and I had it is to receive her months who will
been been the determinators of any life. It
```

## 38 Input: 'She placed the candle on the table '

```text
off freets to the
plancing black which and been on a sort of eyes. We she should be
depend a bed and day in the ladies and the latter dribly of the rooms of
thought beings the boy and they were the rooms of
```

## 39 Input: 'The sound of footsteps came from '

```text
the long of the
Saint-Makin blame and the curical place of the recess was suppose in the
grass the man of the Clanchiew, had had a little words was coming
to the blue of the deader and the world in the bla
```

## 40 Input: 'We waited until morning '

```text
tom free to do of the scape of the
visic of the place of the recess was suppose of the grass the
farter of the cloits and the first in the eyes of the rooms of there the
wilder and standing passed the small of
```
