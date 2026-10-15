import tiktoken

enc = tiktoken.get_encoding("gpt2")
lines = open("../starter_kit/corpus_sample/eng_sample.txt", encoding="utf-8").read().splitlines()

total = total_lower = 0
for i, line in enumerate(lines, 1):
    a = enc.encode(line)
    b = enc.encode(line.lower())
    total += len(a)
    total_lower += len(b)
    if len(a) != len(b):
        print(f"line {i}: {len(a)} -> {len(b)} tokens after lower()")
        print("  ", [enc.decode([t]) for t in a])
        print("  ", [enc.decode([t]) for t in b])

print("english total:", total, "->", total_lower)
