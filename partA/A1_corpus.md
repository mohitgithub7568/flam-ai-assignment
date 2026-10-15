# A1 - corpus

Using FLORES-200 devtest (Meta, CC BY-SA 4.0). Same 1012 sentences
translated into every language, so line 1 in hindi = line 1 in english etc.
https://dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz

Languages: english, hindi, kannada, tamil, telugu, malayalam
(took all 4 dravidian ones instead of just 2)

Size: 1012 sentences each. words: eng 21901, hin 25643, kan 16100,
tam 16763, tel 16936, mal 14924

Domain: wikibooks 351, wikinews 341, wikivoyage 320, so news, how-to and
travel text. (cut -f2 ../flores_download/flores200_dataset/metadata_devtest.tsv | sort | uniq -c)

Cleaning (prep_corpus.py, output in evidence/12_prep_corpus.txt):
- NFC - changed 93 hindi lines, a few in the others
- some tam/tel/mal lines had broken quotes like """text"" from csv export,
  fixed those (~60 lines each)
- collapsed double spaces - kannada had 244 lines with them
english didn't need any cleaning. no lowercasing.

What it can't tell us:
this is formal written text translated from english. real users type short
casual messages, hinglish, hindi in roman script, typos - none of that is
here and it could tokenize quite differently. 1012 sentences is fine for an
average but too small for rare words or specific topics. so it compares the
same content across languages fairly, but it's not what our real traffic
looks like.
