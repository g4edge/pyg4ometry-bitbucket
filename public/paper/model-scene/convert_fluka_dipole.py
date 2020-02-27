import os.path

import pyg4ometry.convert as convert
import pyg4ometry.fluka as fluka
import pyg4ometry.gdml as gdml
import pyg4ometry.visualisation as vi

THISFILE = os.path.abspath(__file__)
THISDIR = os.path.dirname(THISFILE)

def main(vis=False, interactive=False):

    inp = os.path.join(
        THISDIR, "../../../pyg4ometry/test/flairFluka/corrector-dipole.inp")


    reader = fluka.Reader(inp)
    freg = reader.flukaregistry

    greg = convert.fluka2Geant4(freg,
                                worldMaterial="G4_AIR",
                                omitRegions=["airgap", "void"],
                                materialMap={"IRON": "G4_Fe", "COPPER": "G4_Cu"}
    )

    wlv = greg.getWorldVolume()
    wlv.checkOverlaps()

    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(wlv)
        v.setRandomColours()
        v.setOpacity(1)
        v.view(interactive=interactive)


    w = gdml.Writer()
    w.addDetector(greg)

    name = "fluka-dipole"
    gdml_name = "{}.gdml".format(name)
    gmad_name = "{}.gmad".format(name)
    w.write(gdml_name)
    w.writeGMADTesterNoBeamline(gmad_name, gdml_name)





if __name__ == '__main__':
    main(True, True)
