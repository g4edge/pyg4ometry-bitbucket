#!/usr/bin/env python
from IPython import embed
from sys import argv
from os.path import splitext, basename
import StringIO
import bodies
from collections import OrderedDict
from IPython import embed
import re

def main(argv):
    if len(argv) == 0:
        raise IOError("Missing file!")
    if len(argv) > 2:
        raise IOError("Too many files!  Pick just one!")

    file_path = argv[1]
    out_path = basename(splitext(file_path)[0]) + "_logged_python.py"
    with open(file_path) as f:
        lines = f.read().splitlines()

    lines = just_debug_and_error_lines(lines)

    solid_lines = get_solid_lines(lines)
    boolean_lines = get_boolean_lines(lines)
    volume_lines = get_volume_lines(lines)
    world_volume_string = get_world_volume_line(lines)
    # Don't actually need to do anything with this because
    # this will also be in the boolean_lines, albeit not as an error.
    null_mesh_lines = get_null_mesh_lines(lines)

    with open(out_path, 'w') as out:
        write_preamble(out)
        write_wv(world_volume_string, out)
        write_bodies(solid_lines, out)
        write_booleans(boolean_lines, out)
        write_volumes(volume_lines, out)
        write_postamble(out)

# --------input editing functions--------
def just_debug_and_error_lines(lines):  # lines is a list of lines (strings)
    # Remove everything except DEBUG and ERROR lines:
    lines = filter(lambda line: "DEBUG" in line or "ERROR" in line, lines)
    # Keep only after the DEBUG and ERROR flag:
    lines = map(lambda line: re.split("ERROR|DEBUG", line)[1], lines)
    # Delete leading whitespace:
    lines = map(lambda line: line.lstrip(), lines)
    # Delete "Body not instantiated" lines:
    lines = filter(lambda line: not line.startswith("Body not instantiated"),
                   lines)
    return lines

def get_solid_lines(lines):
    solid_lines = filter(lambda line: line.startswith("solid"), lines)
    solid_lines = map(lambda line: line.split("solid: ")[1], solid_lines)
    # Delete duplicate lines as solids are got multiple times...
    solid_lines = list(OrderedDict.fromkeys(solid_lines))
    return solid_lines

def get_boolean_lines(lines):
    boolean_lines = filter(lambda line: line.startswith("boolean"), lines)
    boolean_lines = map(lambda line: line.split("boolean: ")[1], boolean_lines)
    return boolean_lines

def get_volume_lines(lines):
    volume_lines = filter(lambda line: line.startswith("volume"), lines)
    volume_lines = map(lambda line: line.split("volume: ")[1], volume_lines)
    return volume_lines

def get_world_volume_line(lines):
    world_volume_string = filter(lambda line: line.startswith("worldvolume"),
                                 lines)[0]
    world_volume_string = world_volume_string.split("worldvolume: ")[1]
    return world_volume_string

def get_null_mesh_lines(lines):
    null_mesh_string = filter(lambda line: line.startswith("nullmesh"),
                              lines)[0]
    null_mesh_string = null_mesh_string.split("nullmesh: ")[1]
    return null_mesh_string

# ------Writing functions------
def write_wv(wv_string, stream):
    wv_list = wv_string.split("; ")
    wv_list = map(lambda ele: ele.split('=')[1], wv_list)

    wv_name = wv_list[0]
    wv_size = wv_list[1]

    size_defn = "world_size = %s\n" % wv_size

    box_defn = "world_box = pygdml.solid.Box(\"{0}\", {1}, {1}, {1})\n"
    box_defn = box_defn.format(wv_name, "world_size")

    box_vol = (("world_volume = pygdml.Volume("
               "[0,0,0], [0,0,0], world_box, \"%s_volume\","
                "None, 1, False, \"G4_Galactic\")\n") % wv_name)
    stream.writelines([size_defn, box_defn, box_vol, "\n"])

def write_bodies(solid_lines, stream):
    solid_lines = _get_values(solid_lines)
    for line in solid_lines:
        type = line[0]
        name = line[1]
        parameters = eval(line[2])
        out_string = "{1} = pygdml.{0}(\"{1}\", *{2})\n".format(type, name, parameters)
        stream.write(out_string)
    stream.write("\n")


def write_booleans(boolean_lines, stream):
    boolean_lines = _get_values(boolean_lines)

    for line in boolean_lines:
        type = line[0]
        out_name = line[1]
        first_name = line[2] # name of first solid
        second_name = line[3] # name of second solid
        parameters = line[4]
        out_string = "{1} = pygdml.{0}(\"{1}\", {2}, {3}, {4})\n"
        out_string = out_string.format(type, out_name, first_name,
                                       second_name, parameters)
        stream.write(out_string)
    stream.write('\n')

def write_volumes(volume_lines, stream):
    volume_lines = _get_values(volume_lines)

    for line in volume_lines:
        name = line[0]
        translation = line[1]
        rotation = line[2]
        solid = line[3]

        out_string = ("{3} = pygdml.Volume({0}, {1}, {2}, \"{3}\", world_volume, "
                      "1, False, \"G4_Galactic\")\n")
        out_string = out_string.format(rotation, translation, solid, name)
        stream.write(out_string)
    stream.write('\n')

def write_preamble(stream):
    stream.write("import pygdml\n\n")

def write_postamble(stream):
    stream.write("world_volume.setClip()\n")
    stream.write("mesh = world_volume.pycsgmesh()\n")
    stream.write("viewer = pygdml.VtkViewer()\n")
    stream.write("viewer.addSource(mesh)\n")
    stream.write("viewer.view()\n")

def _get_values(lines):
    lines = map(lambda line: line.split("; "), lines)
    # this abomination gets the rvalues of the assignments and returns
    # a nested list of these values, same shape as before.
    lines = map((lambda line:
                       map(lambda defn: defn.split('=')[1], line)), lines)
    return lines

if __name__== "__main__":
    main(argv)
