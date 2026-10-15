import csv

# B1 - kv cache per token: k and v, 28 layers, 8 kv heads, head_dim 128, 2 bytes (fp16)
kv_per_token = 2 * 28 * 8 * 128 * 2
kv_memory = 0.92 * 24e9 - 4.2e9 * 2 - 1.6e9   # 92% of 24GB minus weights minus overhead
max_tokens = kv_memory / kv_per_token
print("kv bytes per token:", kv_per_token)
print("memory left for kv (GB):", round(kv_memory / 1e9, 2))
print("max tokens in cache:", int(max_tokens))
print("max 4096-token sequences:", round(max_tokens / 4096, 1))
print()

rows = list(csv.DictReader(open("../starter_kit/bench/bench_log.csv")))
print("batch, prompt, kv util predicted, kv util log, reported tok/s, (prompt+gen)/wall, gen/wall, preempted")
for r in rows:
    b, p, g = int(r["batch_size"]), int(r["prompt_len"]), int(r["gen_len"])
    wall = float(r["wall_clock_s"])
    print(b, p, round(b * (p + g) / max_tokens, 2), r["kv_cache_util"], r["reported_tok_s"],
          round(b * (p + g) / wall, 1), round(b * g / wall, 1), r["preempted_seqs"])
