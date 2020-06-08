"""
Utility for plotting directories of samples written by run_profile.py.
Argument is a directory, not a specific file.

python profile_analysis ./profile-results/TAN/
"""

import glob
import os.path
import pickle
import sys
import pathlib

import numpy as np
import matplotlib.pyplot as plt

EXCLUDE = {"solid minimisation", "materials", "length safety"}


def _load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def _backend_from_path(path):
    out = os.path.basename(path)
    out, _ = os.path.splitext(out)
    return out

def _title_from_path(path):
    return str(pathlib.Path(path).name).replace("-", " ")

def _get_missing_tags(files, missing_tags):
    bad_files = set()
    for f in files:
        sample = _load_pickle(f)
        sample_names = sample.sample_names()
        if not set(sample_names).intersection(missing_tags):
            bad_files.add(f)
    return bad_files

def plot_dir_contents(dirpath):
    """Plot a directory containing pyg4ometry.utils.Samples pickle files.

    plot_dir_contents("./profile-results/some-magnet/")
    """

    files = glob.glob(os.path.join(dirpath, "*.pickle"))

    f = _load_pickle(files[0])

    sample_names = f.sample_names(exclude=EXCLUDE)
    n_sample_types = len(sample_names)
    index = np.arange(n_sample_types)
    bar_width = 0.2
    opacity = 0.4

    fig, ax = plt.subplots()
    for i, f in enumerate(files):
        sample = _load_pickle(f)
        these_sample_names = sample.sample_names(exclude=EXCLUDE)
        unique_tags = set(sample_names).symmetric_difference(these_sample_names)
        if unique_tags:
            files_with_missing_tags = _get_missing_tags(files, unique_tags)
            raise ValueError(
                f"Missing tags {unique_tags} in files {files_with_missing_tags}")

        means = sample.means(exclude=EXCLUDE)
        stds = sample.stds(exclude=EXCLUDE)
        xbar = index + i * bar_width
        label = _backend_from_path(f)

        values = np.array(list(means.values())) / 60
        err = np.array(list(stds.values())) / 60

        rects = ax.bar(xbar, values, bar_width,
                       yerr=err,
                       alpha=opacity, #color='b',
                       label=label)
        print(label, means)
        plt.legend(loc="upper right")
    
    ax.set_xticks([r + bar_width for r in range(len(sample_names))])
    ax.set_xticklabels(sample_names)
    ax.set_title(_title_from_path(dirpath))
    ax.set_ylabel("Mean CPU time / minutes")
    ax.set_xlabel("Conversion step")
        
    plt.show()
    

if __name__ == '__main__':
    plot_dir_contents(sys.argv[1])

