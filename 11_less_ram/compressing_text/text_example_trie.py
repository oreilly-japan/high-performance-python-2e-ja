import time
import timeit

import marisa_trie
import memory_profiler
import text_example

if __name__ == "__main__":
    print("RAM at start {:0.1f}MiB".format(memory_profiler.memory_usage()[0]))
    # avoid building a temporary list of words in Python, store directly in the
    # Trie
    t1 = time.time()
    words_trie = marisa_trie.Trie(text_example.readers)
    t2 = time.time()
    print("RAM after creating trie {:0.1f}MiB, took {:0.1f}s".format(memory_profiler.memory_usage()[0], t2 - t1))
    print("The trie contains {} words".format(len(words_trie)))

    assert "zwiebel" in words_trie
    time_cost = sum(
        timeit.repeat(
            stmt="u'zwiebel' in words_trie",
            setup="from __main__ import words_trie",
            number=1,
            repeat=10000,
        )
    )
    print("Summed time to lookup word {:0.4f}s".format(time_cost))

    t1 = time.time()
    words_trie.save("words_trie.saved")
    del words_trie
    print("RAM before loading from disk {:0.1f}MiB".format(memory_profiler.memory_usage()[0]))
    t2 = time.time()
    d = marisa_trie.Trie()
    with open("words_trie.saved", "rb") as f:
        words_trie2 = d.read(f)
    t3 = time.time()
    print(
        "RAM after loading trie from disk {:0.1f}MiB, took {:0.1f}s".format(memory_profiler.memory_usage()[0], t2 - t1)
    )
    print("The trie contains {} words".format(len(words_trie2)))
    print(f"time to save {t2 - t1:f}s, time to load {t3-t2:f}s")
    assert "zwiebel" in words_trie2
    time_cost = sum(
        timeit.repeat(
            stmt="u'zwiebel' in words_trie2",
            setup="from __main__ import words_trie2",
            number=1,
            repeat=10000,
        )
    )
    print("Summed time to lookup word {:0.4f}s".format(time_cost))
