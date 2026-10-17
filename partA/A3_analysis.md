# A3 - corrected comparison

corpus: flores devtest from A1 (1012 parallel sentences per language)
tokenizers: gpt2 (what the intern used) and sarvam-1 (made for indian languages)
denominators: per sentence and per word
script: partA/a3.py, output in evidence/10_a3.txt

tokens per sentence vs english:
gpt2: hin 7.42x, kan 13.57x, tam 15.53x, tel 12.96x, mal 15.15x
sarvam-1: hin 1.13x, kan 1.19x, tam 1.15x, tel 1.13x, mal 1.35x

per word gives a different answer for the same text. with sarvam-1, kannada is 1.62x per word but 1.19x per sentence, and hindi is 0.97x per word but 1.13x per sentence. kannada/tamil etc join words so they have fewer words (kan 16100 vs eng 21901, evidence/12) and look worse per word. hindi has more words (25643) because में, की, है are separate, so it looks better.

which number to use: tokens per sentence vs english. the sentences mean the same thing in every language, so it's the number of tokens it costs to say the same thing - which is what we pay for. per word depends on how a language builds words, not on cost.

also the gap is mostly the tokenizer. with sarvam-1 these languages are only 1.1-1.35x english, not 6x.
