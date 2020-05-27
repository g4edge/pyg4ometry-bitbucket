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

def plot_dir_contents(dirpath):
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
        means = sample.means(exclude=EXCLUDE)
        stds = sample.stds(exclude=EXCLUDE)
        xbar = index + i * bar_width
        label = _backend_from_path(f)
        rects = ax.bar(xbar, means.values(), bar_width,
                       yerr=stds.values(),
                       alpha=opacity, #color='b',
                       label=label)
        plt.legend(loc="upper right")
    
    ax.set_xticks([r + bar_width for r in range(len(sample_names))])
    ax.set_xticklabels(sample_names)
    ax.set_title(_title_from_path(dirpath))
    ax.set_ylabel("Mean duration / s")
    ax.set_xlabel("Conversion step")
        
    plt.show()
    

if __name__ == '__main__':
    plot_dir_contents(sys.argv[1])

