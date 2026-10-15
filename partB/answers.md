# Part B

All numbers from partB/calc.py (output in calc_output.txt).

## B1
kv per token = 2 (k and v) x 28 layers x 8 kv heads x 128 head_dim x 2 bytes
= 114,688 bytes (112 KB)

memory for kv = 0.92 x 24 GB - 8.4 GB weights (4.2B x 2 bytes) - 1.6 GB overhead
= 12.08 GB

12.08 GB / 114,688 = ~105,300 tokens. / 4096 = 25.7, so about 25
sequences of 4096 tokens at the same time.

checking against the log: 3584 prompt + 512 gen = 4096 exactly.
batch 24 -> 24 x 4096 / 105,329 = 0.93, log kv_cache_util is 0.93 and
nothing preempted. batch 32 would need 1.24, the log caps at 0.97 and 7
seqs get preempted. short prompts batch 64 -> 0.47, log 0.47. every row
that fits matches the log.

## B2
long prompt sweep: reported_tok_s goes 565 -> 903 -> 1311 -> 1607 at
batch 24, then drops to 1384 (batch 32) and 1298 (batch 48). bigger batch,
lower throughput.

why: only ~25 sequences of 4096 fit (B1). at batch 32 and 48 kv_cache_util
hits 0.97 and preempted_seqs is 7 and 23. the scheduler throws sequences
out of the cache and recomputes them later, so work is done twice and the
rest wait. you can see it in wall_clock_s (61 -> 95 -> 151) and
ttft_ms_p50 (500 -> 637 -> 955). itl_ms_p50 stays ~100 because only ~25
are actually running at once.

fix: set max_num_seqs = 24, so extra requests wait in the queue instead of
being preempted. prediction for batch 48: two clean rounds of 24, each
like the batch 24 row (61.16 s) -> ~122 s instead of 151 s, about 1600
reported tok/s instead of 1298 (~24% more). for batch 32 it wouldn't help
much since the second round is only 8.

## B3
the misread column is reported_tok_s. it's prompt + generated tokens
divided by wall clock: 24 x (3584 + 512) / 61.16 = 1607, same as the log
(matches every row). long prompts have 7x more prompt tokens and those get
processed quickly in one go, so the number looks bigger, but it isn't more
output.

honest goodput, batch 24 long prompt row:
1) generated tokens / wall clock = 24 x 512 / 61.16 = 201 tok/s
2) from inter-token latency: each request makes a token every 96.07 ms,
   so 24 / 0.09607 = 250 tok/s while decoding (higher because it leaves
   out the prefill / waiting for the first token)
so ~200-250 tok/s of real output, not 1607.

short prompts actually give more output: batch 16 short = 294 tok/s vs
batch 16 long = 164 tok/s. and batch 48 is already in the log: 1298
reported, 162 real, not 3200.

what the report should have said: one L4 gives ~200 tok/s of output for
4k-context requests and it stops going up after ~24-25 concurrent requests
because the kv cache is full. plan capacity as ~25 concurrent 4k sequences
per L4, not linear in batch size.

## B4
vllm's preemption counter (vllm:num_preemptions_total). if B2 is right it
stays 0 for every run up to batch 24 and only goes up at batch 32 and 48,
by at least 7 and 23 (more if the same sequence gets preempted twice).
with max_num_seqs = 24 it should stay 0. if it's 0 at batch 48, the slowdown
is something else and B2 is wrong.
