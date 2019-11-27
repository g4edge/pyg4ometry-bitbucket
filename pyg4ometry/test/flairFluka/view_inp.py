import sys

from pyg4ometry.fluka import Reader
import pyg4ometry.visualisation as vi



def main(filein):
    r = Reader(filein)
    g = r.flukaregistry.toG4Registry()

    v = vi.VtkViewer()
    v.addAxes(length=20)
    v.addLogicalVolume(g.getWorldVolume())
    v.view(True)



if __name__ == '__main__':
    main(sys.argv[1])

