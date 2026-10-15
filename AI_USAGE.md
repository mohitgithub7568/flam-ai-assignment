# AI usage

I used Claude (in VS Code) through the whole assignment, mostly like a
tutor. it explained the things I didn't know, drafted most of the scripts
and write-ups, and helped me word the notebook. I ran every script myself,
checked the numbers against the output files, and can explain each part.
These are the places I really needed it:

part A
- finding a way to download FLORES without a huggingface login
- spotting the broken """quotes""" in the tamil/telugu/malayalam files and
  what NFC actually does (hindi had 93 lines where it matters)
- the difference between mean of per-line ratios and total / total
- how to prove random.seed and NFC are harmless instead of just saying it
- loading sarvam-1 with transformers

part B
- the kv cache formula - using the 8 kv heads not the 24 attention heads,
  and the 2x for k and v
- that reported_tok_s includes the prompt tokens, and the second way to
  get goodput from itl
- vllm terms like max_num_seqs and the preemption counter

part C
- the 6 x params x tokens rule for training cost

other
- git commands, and making my english notes clearer


# where it misled me

- it first said the train sentence was the only real translation pair in
  the sample files. reading them again, there are 3.
- from that one pair it looked like per word always makes hindi look
  worse. on flores, per word actually makes hindi look cheaper (0.97x), so
  I stopped trusting conclusions from one sentence.

