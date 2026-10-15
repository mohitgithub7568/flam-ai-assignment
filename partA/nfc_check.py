# same word दफ़्तर stored two ways - फ़ as one code point, or फ + nukta dot
import unicodedata
import tiktoken

enc = tiktoken.get_encoding("gpt2")
one = "द\u095e\u094dतर"
two = "द\u092b\u093c\u094dतर"

print("look the same:", one, two, " equal?", one == two)
print("gpt2 tokens without NFC:", len(enc.encode(one)), len(enc.encode(two)))
a = unicodedata.normalize("NFC", one)
b = unicodedata.normalize("NFC", two)
print("gpt2 tokens with NFC:   ", len(enc.encode(a)), len(enc.encode(b)))
