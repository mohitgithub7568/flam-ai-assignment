# one of the 3 real translation pairs in corpus_sample (eng line 5 = hin line 6)
# 3 tokenizers, and hindi/english ratio with 3 different denominators
import tiktoken

en = "The train arrived exactly on time."
hi = "ट्रेन ठीक समय पर पहुँची।"

print("words:", len(en.split()), len(hi.split()), " chars:", len(en), len(hi))
print()
print("tokenizer      en  hi  per sentence  per word  per char")
for name in ["gpt2", "cl100k_base", "o200k_base"]:
    enc = tiktoken.get_encoding(name)
    e = len(enc.encode(en))
    h = len(enc.encode(hi))
    per_sent = h / e
    per_word = (h / len(hi.split())) / (e / len(en.split()))
    per_char = (h / len(hi)) / (e / len(en))
    print(f"{name:<14}{e:>3}{h:>4}{per_sent:>14.2f}{per_word:>10.2f}{per_char:>10.2f}")
