import sys
import glob
import os

import pyg4ometry.fluka as fluka
import pyg4ometry.visualisation as vi
import pyg4ometry.gdml as gdml
from pyg4ometry.convert import fluka2Geant4

def run_one_test(filein, vis=False, interactive=False):
    r = fluka.Reader(filein)

    greg = fluka2Geant4(r.flukaregistry)

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


def run_all_tests(vis=False, interactive=False):
    total = 0
    passed = 0
    failed = 0

    for f in glob.glob("*.inp"):
        total += 1
        try:
            run_one_test(f, vis=vis, interactive=interactive)
            passed += 1
        except Exception as e:
            print("------> Test {} FAILED with message: {}".format(f, e))
            failed += 1
            continue

    print("{} tested.  {} passed.  {} failed.".format(total, passed, failed))

if __name__ == '__main__':
    run_all_tests()
