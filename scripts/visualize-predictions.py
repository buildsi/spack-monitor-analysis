#!/usr/bin/env python

# Usage:
# starting with a results file in your ~/.spack/analyzers/spack-monitor, run as follows:
# python visualize-predictions.py ~/.spack/spack-monitor/analysis/curl/symbolator-predictions.json
# Note the directory name is the package being spliced

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import shutil
import pandas
import sys
import json
import os

here = os.path.dirname(__file__)


def read_json(filename):
    with open(filename, "r") as fd:
        content = json.loads(fd.read())
    return content


def plot_heatmap(df, save_to=None):
    sns.set_theme(style="white")

    f, ax = plt.subplots(figsize=(30, 30))
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    p = sns.heatmap(
        df, cmap=cmap, center=0, square=True, linewidths=0.5, cbar_kws={"shrink": 0.5}
    )
    p.tick_params(labelsize=5)
    p.set_xlabel("Splice", fontsize=12)
    p.set_ylabel("Binary", fontsize=12)

    if save_to:
        plt.savefig(save_to)
    return plt


def main(result_file):
    if not os.path.exists(result_file):
        sys.exit("Cannot find %s" % result_file)
    data = read_json(result_file)

    # Directory name is package spliced
    package = os.path.basename(os.path.dirname(result_file))

    print("Found predictions for %s %s binaries!" % (len(data), package))

    # First assemble row and column names
    rows = set(data.keys())
    cols = set()
    for binary, results in data.items():
        [cols.add(x["specB"]) for x in results]

    print("Found %s total libraries that were spliced in!" % len(cols))
    cols = sorted(list(cols))
    rows = sorted(list(rows))

    # 0 will mean "I don't know," 1 is "yes this will work" and -1 "this won't work"
    df = pandas.DataFrame(0, index=rows, columns=cols)

    # Populate the data frame
    count = 0
    for binary, results in data.items():
        print("Adding results for %s: %s of %s" % (binary, count, len(data)))
        for result in results:
            # Yes, this will splice
            if result["prediction"]:
                df.loc[binary, result["specB"]] = 1
            else:
                df.loc[binary, result["specB"]] = -1
        count += 1

    # Save the data frame to file
    result_dir = os.path.join(here, "results", package)
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    # Copy the original data file there
    copied_file = os.path.join(result_dir, os.path.basename(result_file))
    shutil.copyfile(result_file, copied_file)
    result_file = os.path.join(result_dir, "%s.csv" % package)
    df.to_csv(result_file)
    save_to = os.path.join(result_dir, "%s.pdf" % package)
    plot_heatmap(df, save_to)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Please provide the path to analysis results!")
    main(sys.argv[1])
