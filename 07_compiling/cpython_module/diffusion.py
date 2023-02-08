import time

import numpy as np
from cdiffusion import evolve

grid_shape = (512, 512)


def run_experiment(num_iterations):
    scratch = np.zeros(grid_shape, dtype=np.double)
    grid = np.zeros(grid_shape, dtype=np.double)

    block_low = int(grid_shape[0] * 0.4)
    block_high = int(grid_shape[0] * 0.5)
    grid[block_low:block_high, block_low:block_high] = 0.005

    start = time.time()
    for i in range(num_iterations):
        evolve(grid, scratch, 1.0, 0.1)
        grid, scratch = scratch, grid
    return time.time() - start


if __name__ == "__main__":
    t = run_experiment(500)
    print(t)
