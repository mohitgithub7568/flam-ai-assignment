# Part C - casual replies in indian languages

**Recommendation:** (a) a small SFT (LoRA) on our model, with (c)
prompt-only as the day 1 baseline. if prompting alone is already good
enough on day 1, ship (c) and skip SFT.
why SFT can beat the same prompt: when making training data offline we can
generate a few versions and keep only the good ones, live we can't filter,
and a long few-shot prompt costs extra tokens on every request.
not (b): it adds a second model to every reply (more latency and GPU),
models under 1B are weak at indian languages, it can change the meaning,
and it needs the same training data as (a) anyway.

**Assumptions**
- our assistant is the 4.2B model from part B and we can fine-tune it
- "casual" = how people actually talk, including common english words
- the model already writes correct (just formal) text in all 6 languages
- the reviewer can rate ~60 short replies per hour
- nobody can check tamil, telugu, bengali, marathi by hand

**Back of envelope**
- data: 1,000 pairs per language x 6 = 6,000 pairs, made by our own model
  (few-shot "rewrite this reply casually"), ~150 tokens each = ~0.9M
  tokens, under an hour on the A100
- training: 6,000 pairs x ~300 tokens x 3 epochs = 5.4M tokens.
  6 x 4.2B x 5.4M = ~1.4e17 FLOPs. A100 ~312 TFLOPS, at ~40% = ~125
  TFLOPS -> ~20 min per run, so lots of runs fit in 2 weeks. 8.4 GB of
  weights + LoRA fits easily in 80 GB
- serving: same model, same tokens, no extra cost (b would add a model)
- reviewer: 10 h/week x 3 weeks = 30 h = ~1,800 ratings. week 1 ~300
  (day 1 test + checking the synthetic data), weeks 2-3 ~800 (200 replies
  x 2 languages x baseline vs SFT), rest spare

**Success metric:** blind test by the reviewer on 200 hindi + 200 kannada
replies: at least 70% rated "sounds casual and natural", and at most 5%
with wrong or changed meaning.

**Kill criterion:** by day 7, if the SFT model wins less than 60% of 100
blind comparisons against prompt-only (hindi + kannada), or meaning errors
go above 5%, drop SFT and ship prompt-only.

**Day 1 experiment:** 50 hindi + 50 kannada real user prompts, answered by
the current model with a casual system prompt and 3 examples. reviewer
rates all 100 (~2 h): casual? meaning ok? that's the baseline for
everything. if it's already 70%+ casual, ship (c).

**Biggest risk:** tamil, telugu, bengali and marathi can't be checked by a
human. launch hindi + kannada first and keep the others behind a flag
until we have reviewers.
