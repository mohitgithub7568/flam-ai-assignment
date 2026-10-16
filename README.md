# Flam AI intern assignment - the audit

- NOTEBOOK.md - lab notebook
- AI_USAGE.md
- partA/ - tokenizer audit: A1_corpus.md, A2_audit.md, A3_analysis.md, A4_memo.md
- partB/answers.md - capacity
- partC/memo.md - decision memo

Outputs of every run are in partA/evidence/ and partB/calc_output.txt.

## setup
run everything from this folder. the scripts expect the starter kit next
to it (../starter_kit).

    python3 -m venv .venv
    source .venv/bin/activate
    pip install tiktoken==0.14.0 transformers==5.20.0

only needed to rebuild the corpus (prep_corpus.py), flores goes in ../flores_download:

    mkdir ../flores_download && cd ../flores_download
    curl -L -o flores200.tar.gz https://dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz
    tar -xzf flores200.tar.gz && cd -

## examples

    python partA/fertility_fixed.py --corpus eng=partA/corpus/eng.txt --corpus hin=partA/corpus/hin.txt
    python partA/a3.py
    python partB/calc.py

## what I found

part A
- the report's 5.89x is gpt2, on 10 sentences that aren't translations of
  each other, measured per word
- fixing the 3 code bugs (split, lower, averaging) only gives 6.11x, so the
  code bugs aren't why the report is wrong. random.seed and NFC look odd
  but are fine
- on flores (1012 parallel sentences), tokens per sentence vs english:
  gpt2 hindi 7.42x, dravidian 13-15x. sarvam-1 only 1.13-1.35x. so it's
  mostly the tokenizer, not the language
- per word is misleading - kannada looks worse and hindi looks cheaper than
  english. tokens per parallel sentence is the number to use

part B
- kv cache is 114,688 bytes per token, so ~25 sequences of 4096 fit on the L4
- past batch 24 the cache is full, sequences get preempted and throughput
  drops (1607 -> 1384 -> 1298)
- reported_tok_s counts prompt tokens too. real output at batch 24 is
  ~201 tok/s, not 1607

part C
- small LoRA SFT, but test prompt-only on day 1 first and ship that if
  it's already good enough
