import os
import unicodedata

src = "../flores_download/flores200_dataset/devtest"
langs = {"eng": "eng_Latn", "hin": "hin_Deva", "kan": "kan_Knda",
         "tam": "tam_Taml", "tel": "tel_Telu", "mal": "mal_Mlym"}

os.makedirs("partA/corpus", exist_ok=True)

for lang, code in langs.items():
    lines = open(f"{src}/{code}.devtest", encoding="utf-8").read().splitlines()
    out = []
    nfc = quotes = spaces = 0
    for line in lines:
        if unicodedata.normalize("NFC", line) != line:
            nfc += 1
            line = unicodedata.normalize("NFC", line)

        # tam/tel/mal have lines like """text"" (csv escaping)
        if line.startswith('"') and line.endswith('"') and '""' in line:
            quotes += 1
            while line.startswith('"') and line.endswith('"') and '""' in line:
                line = line[1:-1].replace('""', '"')
            line = line.replace('""', '"')

        fixed = " ".join(line.split())
        if fixed != line:
            spaces += 1
        out.append(fixed)

    open(f"partA/corpus/{lang}.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
    words = sum(len(x.split()) for x in out)
    print(lang, len(out), "lines | nfc:", nfc, "quotes:", quotes, "spaces:", spaces, "| words:", words)
