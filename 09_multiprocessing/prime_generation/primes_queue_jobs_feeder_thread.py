import argparse
import math
import multiprocessing
import threading
import time
from multiprocessing import Pool

FLAG_ALL_DONE = b"WORK_FINISHED"
FLAG_WORKER_FINISHED_PROCESSING = b"WORKER_FINISHED_PROCESSING"


def check_prime(possible_primes_queue, definite_primes_queue):
    while True:
        n = possible_primes_queue.get()
        if n == FLAG_ALL_DONE:
            # flag that our results have all been pushed to the results queue
            definite_primes_queue.put(FLAG_WORKER_FINISHED_PROCESSING)
            break
        else:
            if n % 2 == 0:
                continue
            for i in range(3, int(math.sqrt(n)) + 1, 2):
                if n % i == 0:
                    break
            else:
                definite_primes_queue.put(n)


def feed_new_jobs(number_range, possible_primes_queue, nbr_poison_pills):
    print("ADDING JOBS TO THE QUEUE")
    for possible_prime in number_range:
        possible_primes_queue.put(possible_prime)
    # add poison pills to stop the remote workers
    for n in range(nbr_poison_pills):
        possible_primes_queue.put(FLAG_ALL_DONE)
    print("ALL JOBS ADDED TO THE QUEUE")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Project description")
    parser.add_argument("nbr_workers", type=int, help="Number of workers e.g. 1, 2, 4, 8")
    args = parser.parse_args()
    print(args)

    primes = []

    manager = multiprocessing.Manager()
    possible_primes_queue = manager.Queue()  # We could limit the input queue size with e.g. `maxsize=3`
    definite_primes_queue = manager.Queue()

    pool = Pool(processes=args.nbr_workers)
    processes = []
    for _ in range(args.nbr_workers):
        p = multiprocessing.Process(target=check_prime, args=(possible_primes_queue, definite_primes_queue))
        processes.append(p)
        p.start()

    t1 = time.time()
    # number_range = range(100000000, 100010000)  # A
    # number_range = range(100000000, 100100000)  # B
    number_range = range(100000000, 101000000)  # C
    # number_range = range(1000000000, 1000100000)  # D
    # number_range = range(100000000000, 100000100000)  # E

    thrd = threading.Thread(target=feed_new_jobs, args=(number_range, possible_primes_queue, args.nbr_workers))
    thrd.start()

    print("NOW WAITING FOR RESULTS...")
    processors_indicating_they_have_finished = 0
    while True:
        new_result = definite_primes_queue.get()  # block whilst waiting for results
        if new_result == FLAG_WORKER_FINISHED_PROCESSING:
            print("WORKER {} HAS JUST FINISHED".format(processors_indicating_they_have_finished))
            processors_indicating_they_have_finished += 1
            if processors_indicating_they_have_finished == args.nbr_workers:
                break
        else:
            primes.append(new_result)
    assert processors_indicating_they_have_finished == args.nbr_workers

    print("Took:", time.time() - t1)
    print(len(primes), primes[:10], primes[-10:])
