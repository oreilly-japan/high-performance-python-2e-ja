import argparse
import pickle

import matplotlib as mpl
import matplotlib.pyplot as plt
import morris_counter

MAX_COUNT = 1_000_000
NBR_MORRIS_COUNTERS_TO_TRY = 3
PICKLE_FILENAME = "12_show_morris_counter.pickle"
PNG_FILENAME = "12_show_morris_counter.png"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Project description")
    parser.add_argument("--build", action="store_true", default=False, help="required positional argument")
    args = parser.parse_args()
    print(args)

    if args.build:
        values_we_count = list(range(MAX_COUNT))
        trials_of_morris_counting = []
        for trial in range(NBR_MORRIS_COUNTERS_TO_TRY):
            mc = morris_counter.MorrisCounter()
            values_in_morris_counter = []
            for n in values_we_count:
                mc.add()
                values_in_morris_counter.append(mc.get())
            trials_of_morris_counting.append(values_in_morris_counter)
        pickle.dump(
            (values_we_count, trials_of_morris_counting, values_in_morris_counter),
            open(PICKLE_FILENAME, "wb"),
        )
    else:
        print("Loading from", PICKLE_FILENAME, " writing to", PNG_FILENAME)
        (values_we_count, trials_of_morris_counting, values_in_morris_counter) = pickle.load(
            open(PICKLE_FILENAME, "rb")
        )
        plt.figure(1)
        plt.clf()

        plt.plot(
            values_we_count,
            values_we_count,
            "-k",
            linewidth=3,
            label="Integer counter (Many bytes)",
        )
        line_style = ["--", "-.", ":"]
        for counter, values_in_morris_counter in enumerate(trials_of_morris_counting):
            plt.plot(
                values_we_count,
                values_in_morris_counter,
                line_style[counter],
                alpha=0.8,
                label="Morris counter {} (1 byte)".format(counter),
            )
        plt.title("Morris counter behavior")
        plt.legend(loc=2, fancybox=True, framealpha=0.8)
        plt.xlabel("Iteration")
        plt.ylabel("Count")

        ax = plt.gca()
        ax.get_xaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
        ax.get_yaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
        # plt.show()
        plt.tight_layout()
        plt.savefig(PNG_FILENAME)
