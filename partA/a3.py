import tiktoken
from transformers import AutoTokenizer

langs = ["eng", "hin", "kan", "tam", "tel", "mal"]

gpt2 = tiktoken.get_encoding("gpt2")
sarvam = AutoTokenizer.from_pretrained("sarvamai/sarvam-1")
tokenizers = {
    "gpt2": gpt2.encode,
    "sarvam-1": lambda s: sarvam.encode(s, add_special_tokens=False),
}

for name, encode in tokenizers.items():
    print(name)
    print("lang, tok/sentence, tok/word, vs eng per sentence, vs eng per word")
    for lang in langs:
        lines = open(f"partA/corpus/{lang}.txt", encoding="utf-8").read().splitlines()
        tokens = sum(len(encode(s)) for s in lines)
        words = sum(len(s.split()) for s in lines)
        per_sent = tokens / len(lines)
        per_word = tokens / words
        if lang == "eng":
            eng_sent, eng_word = per_sent, per_word
        print(lang, round(per_sent, 1), round(per_word, 2), round(per_sent / eng_sent, 2), round(per_word / eng_word, 2))
    print()
