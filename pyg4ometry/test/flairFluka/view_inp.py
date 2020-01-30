import logging
import os
import sys

from pyg4ometry.fluka import FlukaRegistry, Reader
from pyg4ometry.convert import fluka2Geant4
# import pyg4ometry.visualisation as vi
import pyg4ometry.gdml as gdml


def main(filein, debug=False):
    if debug:
        logging.getLogger("pyg4ometry.fluka.region").setLevel(logging.DEBUG)
        logging.getLogger("pyg4ometry.fluka.fluka_registry").setLevel(logging.DEBUG)

    r = Reader(filein)
    arb = r.flukaregistry.bodyDict["arb"]
    # arb._verticesAreClockwise()
    arb.geant4Solid(None)
    from IPython import embed; embed()
    # greg = fluka2Geant4(r.flukaregistry,
    #                     with_length_safety=True,
    #                     split_disjoint_unions=True,
    #                     minimise_solids=True,
    # )

    # wlv = greg.getWorldVolume()
    # wlv.checkOverlaps()
    # v = vi.VtkViewer()
    # v.addAxes(length=200)
    # v.addLogicalVolume(wlv)
    # v.view(True)

    # w = gdml.Writer()
    # w.addDetector(greg)
    # gdml_name = filein.rstrip(".inp") + ".gdml"
    # gmad_name = filein.rstrip(".inp") + ".gmad"
    # w.write(os.path.join(os.path.dirname(__file__), gdml_name))
    # w.writeGmadTester(gmad_name, gdml_name)


if __name__ == '__main__':
    main(sys.argv[1])
