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


## Entry 3 - 15 Oct - testing each suspect one by one

Hypothesis: the code bugs I found in entry 1 are why the report says 5.89x.
if I fix them the number should change a lot.

Experiment: copied fertility.py to partA/fertility_audit.py, changed one
thing at a time, ran it, saved output in partA/evidence/, then git restore.

Results (hin/eng ratio, baseline 5.89x):
- removed random.seed + import -> 5.89x, no change, never used. harmless
- removed NFC -> 5.89x, no change on these files. but दफ़्तर stored 2
  different ways gives 10 vs 12 gpt2 tokens, NFC makes both 12. so it's
  actually useful, keep it
- split() instead of split(" ") -> 5.92x. eng 1.27->1.28, hin 7.45->7.60
- no lower() -> 6.06x. only english changes. thursday, nasa, gpu each
  become 2 tokens when lowercased, so english had 3 extra tokens (99 vs 96).
  I guessed it would go down - I was right

- total tokens / total words instead of per line average -> 5.91x
  I guessed it would change a lot - I was wrong
- all 3 fixes together (fertility_fixed.py) -> 6.11x

Revision: I was wrong, the code bugs only move it ~4% and actually make
hindi look worse not better. so the code bugs are not the main problem.
the bigger problems are the tokenizer (5.7x -> 1.3x in entry 2), the files
not being translations, and dividing by words at all.
tried 3 denominators on the one real pair (train sentence): per word 6.86x,
per char 8.1x, per sentence 5.71x. same tokens, 3 different answers.
per sentence is what actually matters for cost because the meaning is the
same. need a real parallel corpus to do this properly.


## Entry 4 - 15 Oct - there are 3 real pairs, not 1

in entry 3 I used only the train sentence as "the one real pair". went
back to the files and there are actually 3 real translations:
eng 4 = hin 7 (cricket), eng 5 = hin 6 (train), eng 8 = hin 4 (mysuru)

python partA/real_pairs.py -> all 3 pairs added together:
gpt2 6.25x, cl100k 4.08x, o200k 1.39x per sentence. so the tokenizer
result still holds.

surprise: per word = per sentence here (6.25 = 6.25) because both sides
have 19 words. with only the train pair per word was 6.86 vs 5.71, so I
thought per word always makes it look worse. that was too much from one
sentence. per word only goes wrong when the languages use different
numbers of words for the same meaning - probably tamil/kannada, need a
real corpus to check. per char is still off (7.47 vs 6.25).


## Entry 5 - 15 Oct - real corpus + redoing the comparison

Hypothesis: on real parallel text with an indian tokenizer the gap should
be a lot smaller than 5.89x. and per word should hurt tamil/kannada since
they join words.

Experiment: flores devtest, 6 languages (prep_corpus.py). counted tokens
with gpt2 and sarvam-1, per sentence and per word (a3.py).

Result: gpt2 hindi 7.42x per sentence, dravidian 13-15x. sarvam-1 only
1.13-1.35x. kannada per word 1.62x vs 1.19x per sentence, so yes per word
makes it look worse.
surprise: with sarvam-1 hindi per word is 0.97x, cheaper than english.
didn't expect per word to go the other way. it's because hindi has more
words than english for the same sentence.
also kannada had 244 lines with double spaces, the intern's split(" ")
would have counted fake words in all of them.

Revision: per sentence vs english is the number to use.


## Entry 6 - 16 Oct - part B capacity

Hypothesis: the report's "longer prompts = better throughput" looks off.
guessing reported_tok_s includes the prompt tokens.

Experiment: partB/calc.py - kv bytes per token from model_spec, how many
4096 sequences fit, and recomputed every row of bench_log.

Result: 114,688 bytes per token, ~25.7 sequences of 4096 fit. predicted kv
util matches the log exactly in every row that fits (0.93 at batch 24).
reported_tok_s = (prompt + gen) / wall clock in every row, so yes it counts
the prompt. real output at batch 24 long is only ~201 tok/s.
batch 32 and 48 need more cache than exists -> preemption -> slower.

Revision: report's 3200 tok/s at batch 48 is wrong twice - the log already
has batch 48 at 1298, and only ~162 of that is real output.
