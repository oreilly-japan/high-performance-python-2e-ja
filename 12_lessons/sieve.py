import numpy as np
from numba import jit


@jit(nopython=True)
def primes(N=100000):
    numbers = np.ones(N, dtype=np.uint8)
    for i in range(2, N):
        if numbers[i] == 0:
            continue
        else:
            x = i + i
            while x < N:
                numbers[x] = 0
                x += i
    return np.nonzero(numbers)[0][2:]
