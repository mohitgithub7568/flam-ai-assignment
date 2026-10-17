# A2 - fertility.py audit

fertility_audit.py = untouched copy of the intern's script. For each test I changed one thing, ran it, saved output in evidence/, then git restore.

    python partA/fertility_audit.py --corpus eng=../starter_kit/corpus_sample/eng_sample.txt --corpus hin=../starter_kit/corpus_sample/hin_sample.txt

Baseline (00): eng 1.27, hin 7.45, 5.89x - same as the report.
(only 10 sentences each, so these show direction, not final numbers)

## Code bugs
1. split(" ") (line 62) - double space in eng 7 / hin 10 counts an empty word. split() instead -> eng 1.28, hin 7.60, 5.92x (03). Both languages looked slightly better than they are.
2. lower() (line 60) - only changes english. thursday/nasa/gpu become 2 tokens each when lowercased (96 -> 99 tokens, lower_check.py, 11). removed it -> eng 1.23, hin same, 6.06x (04). Made the gap look smaller.
3. per-line average (lines 64-67) - short lines count as much as long ones. total tokens / total words instead (same analyze() as fertility_fixed.py but keeping lower() and split(" ")) -> eng 1.25, hin 7.40, 5.91x (05). the per-line average made both look slightly worse, gap barely moves.
All 3 fixed (fertility_fixed.py, 06): 6.11x. So the code bugs only change it ~4%, they're not why the report is wrong.

## Looks wrong but is fine
- random.seed (line 25) - random is never used. removed it, output identical (01).
- NFC (line 49) - removed it, output identical (02). It's actually useful:
  दफ़्तर stored two ways gives 10 vs 12 gpt2 tokens, after NFC both 12 (nfc_check.py, 08). keep it.

## Bigger problems
4. Files aren't parallel - eng 1 is about an airport, hin 1 is "मुझे सुबह की चाय बहुत पसंद है". only 3 real pairs: eng 4=hin 7, eng 5=hin 6, eng 8=hin 4. so 5.89x compares different sentences.
5. Wrong tokenizer - on the 3 real pairs (real_pairs.py, 09):
   gpt2 6.25x, cl100k 4.08x, o200k 1.39x. only the tokenizer changed. also our model has 128k vocab, gpt2 ~50k, so gpt2 isn't our tokenizer.
6. Tokens per word is the wrong metric - a "word" isn't the same amount of meaning in every language. for cost, the meaning should stay the same, so tokens per parallel sentence is what matters. train pair (07): per sentence 5.71x, per word 6.86x, per char 8.10x. on the 3 pairs per word = per sentence only because both have 19 words. tamil/kannada join words so they should be hit harder - checking in A3.
7. "both metrics agree so it's robust" - they don't (5.89x vs 7.0x), and both use the same token count, so it's not an independent check.
