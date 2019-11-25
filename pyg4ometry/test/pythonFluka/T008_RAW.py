import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import WED
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka.Vector import Three
import numpy as np

def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()

    vertex = [0, 0, 0]
    direction = Three([3, 3, 3])
    side = Three([-0.5, 1, -0.5])
    other_side = np.cross(side, direction)

    side_length = side.length()

    other_side = 1 * (side_length * other_side /
                     np.linalg.norm(other_side)) # 2x length of other side

    # other_side = [0.5, -1, 0.5]


#     wed = WED("WED_BODY", [0, 0, 0],
# # [10, 10, 10],
#               [10, 0, 0], # one transverse side.
#               [10, 10, 10], # length vector.
#               [0, 10, 0], # the other transverse side.
#               freg)

    wed = WED("WED_BODY",
              vertex,
              side, # one transverse side.
              direction, # length vector.
              other_side, # the other transverse side.
              freg)

    z = Zone()
    z.addIntersection(wed)
    region = Region("WED_REG")
    region.addZone(z)
    freg.addRegion(region)

    greg = freg.toG4Registry()


    # Test extents??
    # clip wv?

    if vis:
        v = vi.VtkViewer()
        v.addAxes()
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}



if __name__ == '__main__':
    Test(True, True)
