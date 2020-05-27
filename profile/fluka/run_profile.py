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

    # wlv = greg.getWorldVolume()
    # wlv.checkOverlaps()
    # v = vi.VtkViewer()
    # # wlv.clipSolid()
    # v.addAxes(length=200)
    # v.addLogicalVolume(wlv)
    # # v.setOpacity(1)
    # # v.setRandomColours()
    # # v.view(True)
    # # vi

def main(filein, extra_name="", ntimes=1):
    timer = Timer()

    if extra_name != "":
        try:
            int(extra_name)
        except ValueError:
            pass
        else:
            raise ValueError(
                "extra_name is coercible to int, you made a mistake")

    for i in range(int(ntimes)):
        print(f"Running sample {i}")
        run_once(filein, timer)

    basename, _ = os.path.splitext(filein)
    backend = backendName()

    basedir = "profile-results"
    outpath = os.path.join(basedir, basename, f"{backend}{extra_name}.pickle")

    timer.samples.writeAppend(outpath, verbose=True)


if __name__ == '__main__':
    main(*sys.argv[1:])
