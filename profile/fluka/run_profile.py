import logging
import os
import sys

from pyg4ometry.fluka import FlukaRegistry, Reader
from pyg4ometry.convert import fluka2Geant4
import pyg4ometry.visualisation as vi
import pyg4ometry.gdml as gdml


def main(filein):
    r = Reader(filein)
    greg = fluka2Geant4(r.flukaregistry,
                        profiling_name=filein.rstrip(".inp"))


if __name__ == '__main__':
    main(sys.argv[1])
