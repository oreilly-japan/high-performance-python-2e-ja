import gensim

FILENAME = "_wordids.txt.bz2"

id2word = gensim.corpora.Dictionary.load_from_text(FILENAME)
print(len(id2word))

SUMMARISED_FILE = "all_unique_words_wikipedia_via_gensim.txt"

print("Summarising input files into one output set of {} words".format(len(id2word)))
with open(SUMMARISED_FILE, "w") as f:
    for word in id2word.values():
        f.write(word + "\n")
