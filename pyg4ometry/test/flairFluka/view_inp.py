import sys
import os

from pyg4ometry.fluka import Reader
import pyg4ometry.visualisation as vi
import pyg4ometry.gdml as gdml


def main(filein):
    r = Reader(filein)
    greg = r.flukaregistry.toG4Registry()

    wlv = greg.getWorldVolume()
    wlv.checkOverlaps()
    v = vi.VtkViewer()
    v.addAxes(length=20)
    v.addLogicalVolume(wlv)
    v.view(True)

    w = gdml.Writer()
    w.addDetector(greg)
    gdml_name = filein.rstrip(".inp") + ".gdml"
    gmad_name = filein.rstrip(".inp") + ".gmad"
    w.write(os.path.join(os.path.dirname(__file__), gdml_name))
    w.writeGmadTester(gmad_name, gdml_name)


if __name__ == '__main__':
    main(sys.argv[1])
