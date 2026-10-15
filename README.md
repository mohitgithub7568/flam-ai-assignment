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
