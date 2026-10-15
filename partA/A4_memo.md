# A4 - memo: tokenizer cost by language

**Corrected numbers** (flores devtest, 1012 parallel sentences, tokens per
sentence vs english):
- gpt2: hindi 7.42x, kannada 13.57x, tamil 15.53x, telugu 12.96x, malayalam 15.15x
- sarvam-1: hindi 1.13x, kannada 1.19x, tamil 1.15x, telugu 1.13x, malayalam 1.35x

The report's 5.89x came from gpt2, on 10 sentences that weren't
translations of each other, measured per word. None of those hold up. The
gap is mostly the tokenizer, not the language - with an indian-language
tokenizer it's only 1.1-1.35x.

**Recommendation:** don't budget 6x for hindi and don't decide routing
from gpt2 numbers - gpt2 isn't our tokenizer (our model has 128k vocab).
First run partA/a3.py with our own tokenizer (one line change). If indian
languages come out close to sarvam-1 (~1.1-1.4x), keep one model and just
budget ~1.4x per indian-language request. Only if they come out way higher,
like gpt2, is it worth routing indian traffic to a model with an
indian-language tokenizer.

**Biggest caveat:** flores is formal text translated from english. real
users send short casual messages, hinglish and hindi in roman script
("kya haal hai"), which can tokenize very differently. so these numbers
are for the same content, not our real traffic.

**Metric to watch in production:** average tokens per message for each
language, divided by english. if it's much higher than what a3.py gives
for our tokenizer, real traffic tokenizes worse than flores and this
analysis is wrong for us.
