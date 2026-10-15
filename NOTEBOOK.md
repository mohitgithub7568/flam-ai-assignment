## Entry 1 - 14 Oct - getting the report's numbers + reading the script

Hypothesis: before calling anything a bug I need the same numbers as the
report, otherwise I have nothing to compare to.

Experiment: ran the intern's script
python fertility.py --corpus eng=corpus_sample/eng_sample.txt --corpus hin=corpus_sample/hin_sample.txt --tokenizer gpt2

Result: eng 1.27, hin 7.45, 5.89x. same as report.
one confusing thing - 7.45/1.27 is 5.87 not 5.89. turns out script uses
the full numbers (7.4485/1.2652) and only rounds when printing.

while reading the files and the code I noticed:
- the hindi and english files are not translations of each other. line 1
  english is about an airport, line 1 hindi is "मुझे सुबह की चाय बहुत पसंद है".
  only around 4 sentences match and those are on different lines
- english line 7 and hindi line 10 have a double space, split(" ") counts
  an empty word there (8 words instead of 7)
- lower() only changes english. NASA is 1 token but nasa is 2
- it averages every line separately instead of total tokens / total words
- len() counts matras as separate characters, किताबें comes out as 7
- random.seed is never used, probably harmless

Revision: these are just doubts right now, not proven. next I'll test
them one by one against 1.27 / 7.45. my guess is the files not being
real translations is a bigger problem than these small code bugs.


## Entry 2 - 15 Oct - is hindi expensive or is the tokenizer bad?

Hypothesis: report says hindi is 5.89x english and that it's because of the
hindi script, not the tokenizer. I believed it at first, hindi has matras
and all so more pieces made sense. If that's true, any tokenizer should
show a big gap.

Experiment: took one sentence in both languages
en - The train arrived exactly on time.
hi - ट्रेन ठीक समय पर पहुँची।
and counted tokens with 3 tokenizers from tiktoken.

Result:
gpt2 - en 7, hi 40 (5.7x)
cl100k (gpt-4) - en 7, hi 25 (3.6x)
o200k (gpt-4o) - en 7, hi 9 (1.3x)
english stays 7 every time, only hindi changes. gpt2 breaks hindi into
broken bytes because every hindi letter is 3 bytes and gpt2 barely knows
hindi. o200k keeps words like समय and ठीक as one token.

Revision: I was wrong. same sentence, only tokenizer changed, and the gap
went from 5.7x to 1.3x. so it's mostly the tokenizer, not hindi. report's
point 3 looks wrong. but this is just 1 sentence, need a proper parallel
corpus to actually say this.

Todo: need an indian language tokenizer for later.
