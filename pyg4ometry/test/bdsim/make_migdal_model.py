import os

import pyg4ometry.gdml as gdml
from pyg4ometry.gdml.Defines import Constant
import pyg4ometry.geant4 as g4
from pyg4ometry.geant4.solid import Box, Subtraction
from pyg4ometry.geant4 import LogicalVolume, PhysicalVolume
import pyg4ometry.visualisation as vi

REG = g4.Registry()

SAFETY = Constant("safety", 1e-3, REG)
ROOM_LENGTH = Constant("room_length", 3.5e3, REG) # mm
ROOM_WIDTH = Constant("room_width", 2.5e3, REG)
ROOM_HEIGHT = Constant("room_height", 3.5e3, REG)

WALL_THICKNESS = Constant("wall_thickness", 1e3, REG)
TOTAL_WIDTH = Constant("total_width", ROOM_WIDTH + 2*WALL_THICKNESS, REG)
TOTAL_LENGTH = Constant("total_length", ROOM_LENGTH + 2*WALL_THICKNESS, REG)
TOTAL_HEIGHT = Constant("total_height", ROOM_HEIGHT + 2*WALL_THICKNESS, REG)

DIVIDING_WALL_WIDTH = Constant("dividing_wall_width", 1.5e3, REG)
DIVIDING_WALL_THICKNESS = Constant("dividing_wall_thickness", 0.2e3, REG)
DIVIDING_WALL_HEIGHT = Constant("dividing_wall_height", 2e3, REG)

DIVIDING_WALL_OFFSET = Constant("dividing_wall_offset", 0.75e3, REG)

DETECTOR_SIDES = Constant("detector_sides", 0.3e3, REG) # 30cm box

BEAM_OFFSET_X = 0.75e3 # millimetres
BEAM_OFFSET_Y = 1.25e3 # millimetres
BEAM_OFFSET_Z = 1e3 # millimetres

DETECTOR_OFFSET_X = Constant("detector_offset_x", 1e3, REG)
DETECTOR_OFFSET_Y = Constant("detector_offset_y", 1.1e3, REG)
DETECTOR_OFFSET_Z = Constant("detector_offset_z", 0.85e3, REG)

CONCRETE = g4.MaterialPredefined("G4_CONCRETE", REG)
DETECTOR_MATERIAL = g4.MaterialPredefined("G4_STAINLESS-STEEL", REG)

BEAM_OFFSET_X = Constant("beam_offset_x", 0.75e3, g4.Registry())
BEAM_OFFSET_Y = Constant("beam_offset_y", 1.25e3, g4.Registry())
BEAM_OFFSET_Z = Constant("beam_offset_z", 1e3, g4.Registry())


def main():
    wlv = make_world(REG)
    make_room(REG, wlv)
    make_dividing_wall(REG, wlv)
    make_detector(REG, wlv)
    wlv.checkOverlaps()
    REG.setWorld(wlv.name)
    v = vi.VtkViewer()
    # v.addAxes(length=2000)
    v.addLogicalVolume(REG.getWorldVolume())
    v.setRandomColours()

    # v.view()

    w = gdml.Writer()
    w.addDetector(REG)
    gdml_name = "migdal.gdml"
    gmad_name = "migdal.gmad"
    w.write(os.path.join(os.path.dirname(__file__), gdml_name))

    make_gmad()



def make_world(reg):
    world_box = Box("world_box",
                    2*TOTAL_LENGTH, # make it 2x bigger than the contents.
                    2*TOTAL_HEIGHT,
                    2*TOTAL_WIDTH,
                    reg)
    wlv = g4.LogicalVolume(world_box,
                           g4.MaterialPredefined("G4_AIR"), "wlv", reg)

    return wlv

def make_room(reg, world_lv):

    room_walls = Box("room_walls",
                     TOTAL_LENGTH,
                     TOTAL_HEIGHT,
                     TOTAL_WIDTH,
                     reg)

    room_hole = Box("room_hole",
                    ROOM_LENGTH+SAFETY,
                    ROOM_HEIGHT+SAFETY,
                    ROOM_WIDTH+SAFETY,
                    reg)

    room_solid = Subtraction("room_solid", room_walls,
                             room_hole, [[0, 0, 0], [0, 0, 0]], reg)

    room_lv = LogicalVolume(room_solid, CONCRETE, "room_lv", reg)
    pv_pos = [0.5*ROOM_LENGTH, 0.5*ROOM_HEIGHT, 0.5*ROOM_WIDTH]
    room_pv = PhysicalVolume([0, 0, 0], pv_pos,
                             room_lv, "room_pv",
                             world_lv,
                             reg)

def make_dividing_wall(reg, world_lv):
    dividing_wall = Box("dividing_wall",
                        DIVIDING_WALL_THICKNESS-SAFETY,
                        DIVIDING_WALL_HEIGHT-SAFETY,
                        DIVIDING_WALL_WIDTH-SAFETY,
                        reg)
    dividing_wall_lv = LogicalVolume(dividing_wall,
                                     CONCRETE,
                                     "dividing_wall_lv",
                                     reg)

    dividing_wall_pv = PhysicalVolume(
        [0, 0, 0], # rotation
        [ROOM_LENGTH - DIVIDING_WALL_OFFSET - 0.5 * DIVIDING_WALL_THICKNESS, # x offset
         0.5 * DIVIDING_WALL_HEIGHT, # y offset
         ROOM_WIDTH - 0.5 * DIVIDING_WALL_WIDTH], # z offset
        dividing_wall_lv,
        "dividing_wall_pv",
        world_lv,
        reg)



def make_detector(reg, world_lv):
    detector = Box("detector_solid", 300,  300, 300, reg)
    detector_lv = LogicalVolume(detector,
                                DETECTOR_MATERIAL, "detector_lv", reg)

    detector_pv = PhysicalVolume(
        [0, 0, 0],
        [DETECTOR_OFFSET_X + 0.5 * DETECTOR_SIDES,
         DETECTOR_OFFSET_Y + 0.5 * DETECTOR_SIDES,
         ROOM_WIDTH - DETECTOR_OFFSET_Z - 0.5 * DETECTOR_SIDES],
        detector_lv,
        "detector_lv",
        world_lv,
        reg)


def make_gmad():
    with open("migdal.gmad", "w") as f:
        f.write('migdal: placement, geometryFile="gdml:./migdal.gdml";\n\n')

        write_gmad_beam(f)
        write_gmad_options(f)
        write_gmad_sampler_placements(f)

def write_gmad_sampler_placements(f):

    half_size = (DETECTOR_SIDES / 2.0 + SAFETY).eval()

    front_x = DETECTOR_OFFSET_X.eval()
    front_y = (DETECTOR_OFFSET_Y + DETECTOR_SIDES/2).eval()
    front_z = (ROOM_WIDTH - DETECTOR_OFFSET_Z - DETECTOR_SIDES/2).eval()

    sp = "samplerplacement"
    aper_string = 'aper1={}*mm, aper2={}*mm, shape="rectangular"'.format(
        half_size, half_size)

    rotation = "axisAngle=1, axisX=0, axisY=1, axisZ=0, angle=pi/2"
    front = "front: {}, x={}*mm, y={}*mm, z={}*mm, {}, {};\n".format(
        sp,
        front_x,
        front_y,
        front_z,
        aper_string,
        rotation
    )

    back_x = (DETECTOR_OFFSET_X + DETECTOR_SIDES).eval()
    back_y = front_y
    back_z = front_z
    rotation = "axisAngle=1, axisX=0, axisY=1, axisZ=0, angle=-pi/2"
    back = "back: {}, x={}*mm, y={}*mm, z={}*mm, {}, {};\n".format(
        sp,
        back_x,
        back_y,
        back_z,
        aper_string,
        rotation
    )



    left_x = (DETECTOR_OFFSET_X + DETECTOR_SIDES / 2.0).eval()
    left_y = front_y
    left_z = (ROOM_WIDTH - DETECTOR_OFFSET_Z - DETECTOR_SIDES).eval()
    rotation = ""
    left = "left: {}, x={}*mm, y={}*mm, z={}*mm, {};\n".format(
        sp,
        left_x,
        left_y,
        left_z,
        aper_string,
    )

    right_x = (DETECTOR_OFFSET_X + DETECTOR_SIDES / 2.0).eval()
    right_y = left_y
    right_z = (ROOM_WIDTH - DETECTOR_OFFSET_Z).eval()
    rotation = "axisAngle=1, axisX=0, axisY=1, axisZ=0, angle=pi"
    right = "right: {}, x={}*mm, y={}*mm, z={}*mm, {}, {};\n".format(
        sp,
        right_x,
        right_y,
        right_z,
        aper_string,
        rotation
    )

    top_x = (DETECTOR_OFFSET_X + DETECTOR_SIDES/2).eval()
    top_y = (DETECTOR_OFFSET_Y + DETECTOR_SIDES).eval()
    top_z = (ROOM_WIDTH - DETECTOR_OFFSET_Z - DETECTOR_SIDES/2.0).eval()
    rotation = "axisAngle=1, axisX=1, axisY=0, axisZ=0, angle=pi/2"
    top = "top: {}, x={}*mm, y={}*mm, z={}*mm, {}, {};\n".format(
        sp,
        top_x,
        top_y,
        top_z,
        aper_string,
        rotation
    )

    bottom_x = (DETECTOR_OFFSET_X + DETECTOR_SIDES/2).eval()
    bottom_y = DETECTOR_OFFSET_Y.eval()
    bottom_z = (ROOM_WIDTH - DETECTOR_OFFSET_Z - DETECTOR_SIDES/2.0).eval()
    rotation = "axisAngle=1, axisX=1, axisY=0, axisZ=0, angle=-pi/2"
    bottom = "bottom: {}, x={}*mm, y={}*mm, z={}*mm, {}, {};\n".format(
        sp,
        bottom_x,
        bottom_y,
        bottom_z,
        aper_string,
        rotation
    )

    f.write(front)
    f.write(back)
    f.write(left)
    f.write(right)
    f.write(top)
    f.write(bottom)

def write_gmad_beam(f):
    f.write("neutron_mass=939.56542052*MeV;\n")
    f.write("neutron_kinetic_energy=14*MeV;\n")

    f.write("""
beam, particle="neutron",
      energy=neutron_mass+neutron_kinetic_energy,
      ! Beam distribution, 3x3cm square beam:
      distrType="square",
      envelopeX=3*cm,
      envelopeY=3*cm,
      envelopeXp=0,
      envelopeYp=0;
""")

def write_gmad_options(f):
    beamlineX = BEAM_OFFSET_X.eval()
    beamlineY = BEAM_OFFSET_Y.eval()
    beamlineZ = (ROOM_WIDTH - BEAM_OFFSET_Z).eval()


    f.write("""
option, ! Choosing which bits to store:
        storeEloss=0,
        storeSamplerKineticEnergy=1,
        ! Beamline rotation:
        beamlineAxisAngle=1,
        beamlineAxisY=1,
        beamlineAngle=pi/2,
        beamlineX={blx}*mm,
        beamlineY={bly}*mm,
        beamlineZ={blz}*mm,
        ! Physics list:
        physicsList="g4QGSP_BIC_HP_EMZ";
""".format(blx=beamlineX, bly=beamlineY, blz=beamlineZ))


if __name__ == '__main__':
    main()
