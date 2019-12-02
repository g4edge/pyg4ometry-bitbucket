import sys
import glob
import os

import pyg4ometry.fluka as fluka
import pyg4ometry.visualisation as vi
import pyg4ometry.gdml as gdml

def run_one(filein, vis=False, interactive=False):
    r = fluka.Reader(filein)
    greg = r.flukaregistry.toG4Registry()

    wlv = greg.getWorldVolume()

    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        wlv.checkOverlaps()
        v.addLogicalVolume(wlv)
        v.view(interactive)


    w = gdml.Writer()
    w.addDetector(greg)
    gdml_name = filein.rstrip(".inp") + ".gdml"
    gmad_name = filein.rstrip(".inp") + ".gmad"
    w.write(os.path.join(os.path.dirname(__file__), gdml_name))
    w.writeGmadTester(gmad_name, gdml_name)


def run_all(vis=False, interactive=False):
    for f in glob.glob("*.inp"):
        print "---> Testing file = {}".format(f)
        run_one(f, vis=vis, interactive=interactive)


def main(f):
    """ Either test an individual file, or if None is provided as the
    argument, test all."""
    if f is None:
        run_all()
    else:
        run_one(f)


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IndexError:
        main(None)

