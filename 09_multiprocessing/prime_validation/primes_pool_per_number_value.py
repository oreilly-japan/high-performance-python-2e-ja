"""Check primality by splitting the list of factors with early prime check and Value"""
import math
import multiprocessing
import timeit
from multiprocessing import Pool

import create_range

SERIAL_CHECK_CUTOFF = 21
CHECK_EVERY = 1000
FLAG_CLEAR = 0  # b'0'
FLAG_SET = 1  # b'1'
print("CHECK_EVERY", CHECK_EVERY)


def check_prime_in_range(n_from_i_to_i):
    (n, (from_i, to_i)) = n_from_i_to_i
    if n % 2 == 0:
        return False
    assert from_i % 2 != 0
    check_every = CHECK_EVERY
    for i in range(from_i, int(to_i), 2):
        check_every -= 1
        if not check_every:
            if value.value == FLAG_SET:
                return False
            check_every = CHECK_EVERY

        if n % i == 0:
            value.value = FLAG_SET
            return False
    return True


def check_prime(n, pool, nbr_processes):
    # cheaply check high probability set of possible factors
    from_i = 3
    to_i = SERIAL_CHECK_CUTOFF
    value.value = FLAG_CLEAR
    if not check_prime_in_range((n, (from_i, to_i))):
        return False
    value.value = FLAG_CLEAR

    from_i = to_i
    to_i = int(math.sqrt(n)) + 1

    ranges_to_check = create_range.create(from_i, to_i, nbr_processes)
    ranges_to_check = list(zip(len(ranges_to_check) * [n], ranges_to_check))
    assert len(ranges_to_check) == nbr_processes
    results = pool.map(check_prime_in_range, ranges_to_check)
    if False in results:
        return False
    return True


if __name__ == "__main__":
    NBR_PROCESSES = 4
    # multiprocessing.set_start_method("fork") # for macOX above Python 3.8
    # note b'c' in Python 2.7 was a 1 byte char https://docs.python.org/2.7/library/array.html#module-array
    # whereas 'b' is a 1 byte signed char in Python 3.7 https://docs.python.org/3.3/library/array.html#module-array
    value = multiprocessing.RawValue("b", FLAG_CLEAR)  # 1 byte character
    pool = Pool(processes=NBR_PROCESSES)
    print("Testing with {} processes".format(NBR_PROCESSES))
    for label, nbr in [
        ("trivial non-prime", 112272535095295),
        ("expensive non-prime18_1", 100109100129100369),
        ("expensive non-prime18_2", 100109100129101027),
        # ("prime", 112272535095293)]:  # 15
        # ("prime17",  10000000002065383)]
        ("prime18_1", 100109100129100151),
        ("prime18_2", 100109100129162907),
    ]:
        # ("prime23", 22360679774997896964091)]:

        time_costs = timeit.repeat(
            stmt="check_prime({}, pool, {})".format(nbr, NBR_PROCESSES),
            repeat=20,
            number=1,
            setup="from __main__ import pool, check_prime",
        )
        print("check_prime returns:", check_prime(nbr, pool, NBR_PROCESSES))
        print("{:19} ({}) {: 3.6f}s".format(label, nbr, min(time_costs)))
