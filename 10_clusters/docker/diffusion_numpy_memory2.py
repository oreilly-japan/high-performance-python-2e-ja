#!/usr/bin/env python3

import time
import timeit

from numpy import add, copyto, multiply, zeros

try:
    profile
except NameError:
    profile = lambda x: x

grid_shape = (256, 256)


def roll_add(rollee, shift, axis, out):
    if shift == 1 and axis == 0:
        out[1:, :] += rollee[:-1, :]
        out[0, :] += rollee[-1, :]
    elif shift == -1 and axis == 0:
        out[:-1, :] += rollee[1:, :]
        out[-1, :] += rollee[0, :]
    elif shift == 1 and axis == 1:
        out[:, 1:] += rollee[:, :-1]
        out[:, 0] += rollee[:, -1]
    elif shift == -1 and axis == 1:
        out[:, :-1] += rollee[:, 1:]
        out[:, -1] += rollee[:, 0]


def laplacian(grid, out):
    copyto(out, grid)
    multiply(out, -4.0, out)
    roll_add(grid, +1, 0, out)
    roll_add(grid, -1, 0, out)
    roll_add(grid, +1, 1, out)
    roll_add(grid, -1, 1, out)


@profile
def evolve(grid, dt, out, D=1):
    laplacian(grid, out)
    multiply(out, D * dt, out)
    add(out, grid, out)


def run_experiment(num_iterations):
    scratch = zeros(grid_shape)
    grid = zeros(grid_shape)

    block_low = int(grid_shape[0] * 0.4)
    block_high = int(grid_shape[0] * 0.5)
    grid[block_low:block_high, block_low:block_high] = 0.005

    start = time.time()
    for i in range(num_iterations):
        evolve(grid, 0.1, scratch)
        grid, scratch = scratch, grid
    return time.time() - start


if __name__ == "__main__":
    n_runs = 100
    runtime = timeit.timeit(f"run_experiment({n_runs})", number=25, globals=globals())
    print(f"Runtime for {n_runs} with grid {grid_shape}: {runtime:0.4f}s")
