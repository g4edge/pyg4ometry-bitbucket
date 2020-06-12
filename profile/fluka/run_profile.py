import pathlib
import json
import logging
import os
import sys

from pyg4ometry.fluka import FlukaRegistry, Reader
from pyg4ometry.convert import fluka2Geant4
import pyg4ometry.visualisation as vi
import pyg4ometry.gdml as gdml
from pyg4ometry.config import backendName
from pyg4ometry.utils import Timer


def run_once(filein, timer):
    r = Reader(filein)
    greg = fluka2Geant4(r.flukaregistry, timer=timer)

def main(filein, extra_name="", ntimes=1):
    """Profile the conversion of a FLUKA model to geant4.

    :param filein: FLUKA inp file to be converted
    :type name: str
    :param extra_name: extra string to append as metadata to the output \
    profiling information to distinguish a given sample.
    :type extra_name: str
    :param ntimes: The number of times to sample the conversion.
    :type ntimes: int

    """
    timer = Timer()

    # Help prevent user from making a mistake by mixing up ntimes and
    # extra_name.
    if extra_name != "":
        try:
            int(extra_name)
        except ValueError:
            pass
        else:
            raise ValueError(
                "extra_name should be a string, not a number")

    # Run the conversion
    backend = backendName()
    for i in range(int(ntimes)):
        i += 1
        ed = ""
        if extra_name:
            ed = f", {extra_name}"
        print(f"Running sample {i} of {ntimes} with {backend}{ed}")
        run_once(filein, timer)

    # Output directory and sample file
    basename, _ = os.path.splitext(filein)
    basedir = "profile-results"
    outpath = os.path.join(basedir, basename, f"{backend}{extra_name}.pickle")

    # Write the output
    try:
        os.makedirs(os.path.dirname(outpath))
    except FileExistsError:
        pass
    timer.samples.writeAppend(outpath, verbose=True)


if __name__ == '__main__':
    main(*sys.argv[1:])
