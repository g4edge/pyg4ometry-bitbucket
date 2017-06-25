import subprocess as _sp
import os.path as _path
import antlr4 as _antlr4

from FlukaLexer import FlukaLexer
from FlukaParser import FlukaParser

def Parse(path):
    if not _path.exists(path):
        raise IOError("File not found: %s" % path)

    with open(path, 'r') as f:
        lines = f.readlines()

    not_geometry, geometry = _separate_geometry(lines)

    # Create _ANTLR4 char stream from processed model string
    # geometry is a list of strings here, so join as single string.
    istream = _antlr4.InputStream(''.join(geometry))

    # Tokenise character stream
    lexed_input = FlukaLexer(istream)

    # Create a buffer of tokens from lexer
    tokens = _antlr4.CommonTokenStream(lexed_input)

    # Create a parser that reads from stream of tokens
    parser = FlukaParser(tokens)

    # Create syntax tree
    tree = parser.geocards()

    return tree


def _separate_geometry(lines):
    """Separate the model into two parts, lines describing the
    geometry, and lines describing what is not the geometry.  In both
    cases, the other is commented out rather than removed.  This is
    useful as the line numbering is retained.

    """
    # Get the two indices of geobegin and geoend
    geo_begin_index = (i for i, line in enumerate(lines)
                       if line.startswith("GEOBEGIN")).next()
    geo_end_index = (i for i, line in enumerate(lines)
                     if line.startswith("GEOEND")).next()

    # Check if line after geobegin is a body definition, if not then
    # it is part of the GEOBEGIN card, and move begin_index onwards one.
    for body_type in _body_types:
        if lines[geo_begin_index + 1].startswith(body_type):
            break
    else: # no break
        geo_begin_index += 1

    # Split the model into 3 parts
    before_geometry = lines[:geo_begin_index + 1]
    geometry = lines[geo_begin_index + 1:geo_end_index]
    after_geometry = lines[geo_end_index:]

    # Create list of equal length of commented lines to preserve line numbers
    commented_before_geometry = ["*\n" for line in before_geometry]
    commented_geometry = ["*\n" for line in geometry]
    commented_after_geometry = ["*\n" for line in after_geometry]
    # Assemble and return the two sets:
    geometry = commented_before_geometry + geometry + commented_after_geometry
    not_geometry = before_geometry + commented_geometry + after_geometry
    return not_geometry, geometry

def VisitModel(tree):

    if visitor != default:
        pass

    visitor = FlukaTreeVisitor()

_body_types = ["ARB", "BOX", "ELL", "PLA", "QUA", "RAW",
               "RCC", "REC", "RPP", "SPH", "TRC", "WED",
               "XCC", "XEC", "XYP", "XZP", "YCC", "YEC",
               "YZP", "ZCC", "ZEC"]
