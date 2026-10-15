# the 3 pairs in corpus_sample that really are translations of each other
# eng 4 = hin 7, eng 5 = hin 6, eng 8 = hin 4 (found by reading both files)
# run from the assignment folder
import tiktoken

eng = open("../starter_kit/corpus_sample/eng_sample.txt", encoding="utf-8").read().splitlines()
hin = open("../starter_kit/corpus_sample/hin_sample.txt", encoding="utf-8").read().splitlines()
pairs = [(eng[3], hin[6]), (eng[4], hin[5]), (eng[7], hin[3])]  # python counts from 0

for en, hi in pairs:
    print(en, "|", hi)

en_words = sum(len(en.split()) for en, hi in pairs)
hi_words = sum(len(hi.split()) for en, hi in pairs)
en_chars = sum(len(en) for en, hi in pairs)
hi_chars = sum(len(hi) for en, hi in pairs)
print()
print("words:", en_words, hi_words, " chars:", en_chars, hi_chars)
print()
print("tokenizer      en   hi  per sentence  per word  per char")
for name in ["gpt2", "cl100k_base", "o200k_base"]:
    enc = tiktoken.get_encoding(name)
    e = sum(len(enc.encode(en)) for en, hi in pairs)
    h = sum(len(enc.encode(hi)) for en, hi in pairs)
    per_word = (h / hi_words) / (e / en_words)
    per_char = (h / hi_chars) / (e / en_chars)
    print(f"{name:<14}{e:>3}{h:>5}{h / e:>14.2f}{per_word:>10.2f}{per_char:>10.2f}")
