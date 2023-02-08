import time
import timeit

import memory_profiler
import text_example

if __name__ == "__main__":
    print("RAM at start {:0.1f}MiB".format(memory_profiler.memory_usage()[0]))
    t1 = time.time()
    words = [w for w in text_example.readers]
    print("Loading {} words".format(len(words)))
    t2 = time.time()
    print("RAM after creating list {:0.1f}MiB, took {:0.1f}s".format(memory_profiler.memory_usage()[0], t2 - t1))

    assert "zwiebel" in words
    time_cost = sum(timeit.repeat(stmt="u'zwiebel' in words", setup="from __main__ import words", number=1, repeat=100))
    time_cost *= 100  # to make it equivalent to 10_000 calls
    print("Summed time to lookup word {:0.4f}s".format(time_cost))
