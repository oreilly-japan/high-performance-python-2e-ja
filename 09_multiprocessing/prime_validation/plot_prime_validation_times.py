import argparse

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Project description")
parser.add_argument(
    "--slow",
    action="store_true",
    default=False,
    help="if present then draw slow result, if not then fast results",
)
args = parser.parse_args()

labels = ["small non-prime", "large non-prime 1", "large non-prime 2", "prime 1", "prime 2"]

times_primes = [0.000001, 4.876819, 8.809977, 16.270211, 16.270211]
times_primes_pool_per_number2 = [0.000001, 4.120791, 4.118397, 4.089632, 4.089632]
times_primes_pool_per_number_redis = [0.000129, 1.618964, 1.348230, 8.339887, 8.401287]
times_primes_pool_per_number_manager = [0.000114, 1.910889, 1.646287, 10.062349, 10.101160]

times_primes_pool_per_number_value = [0.000001, 1.112797, 0.925860, 5.457609, 5.469409]
times_primes_pool_per_number_mmap = [0.000002, 1.107603, 0.921475, 5.425130, 5.442197]
times_primes_pool_per_number_mmap3 = [0.000002, 0.845629, 0.702337, 4.146212, 4.150105]

method_labels_slower = [
    "Serial (No IPC)",
    "Less naive Pool",
    "Redis flag",
    "Manager flag",
]  # , "Manager flag", "Value flag", "MMap flag"]
all_times_slower = [
    times_primes,
    times_primes_pool_per_number2,
    times_primes_pool_per_number_redis,
    times_primes_pool_per_number_manager,
]

method_labels_faster = ["Less naive Pool", "RawValue flag", "MMap flag", "MMap Redux flag"]
all_times_faster = [
    times_primes_pool_per_number2,
    times_primes_pool_per_number_value,
    times_primes_pool_per_number_mmap,
    times_primes_pool_per_number_mmap3,
]

if args.slow:
    png_filename = "multiprocessing_plot_prime_validation_times_slower_results.png"
    print("Writing to", png_filename)
    symbols = ["o", "v", "s", "^", "*", "+", "x"]
    linestyles = ["-", "--", "-.", ":", "-"]
    all_times = all_times_slower
    method_labels = method_labels_slower
    title = "Slower IPC methods"
    ymax = 17
else:
    png_filename = "multiprocessing_plot_prime_validation_times_faster_results.png"
    symbols = ["v", "o", "s", "^", "*", "+", "x"]
    linestyles = ["--", "-", "-.", ":", "-"]
    all_times = all_times_faster
    method_labels = method_labels_faster
    title = "Faster IPC methods"
    ymax = 6

f = plt.figure(1)
plt.clf()

for times, label, symbol, linestyle in zip(all_times, method_labels, symbols, linestyles):
    # plt.scatter(range(len(labels)), times, label=label, marker=symbol)
    plt.plot(list(range(len(labels))), times, label=label, marker=symbol, linestyle=linestyle)

plt.title(title)
plt.legend(loc="upper left")
plt.ylabel("Time in seconds (smaller is better)")
plt.xticks(list(range(len(labels))), labels, rotation=45, ha="right")
plt.xlim(xmin=-0.1, xmax=len(labels) - 0.9)
plt.ylim(ymin=-0.1, ymax=ymax)
plt.tight_layout()
plt.savefig(png_filename)
