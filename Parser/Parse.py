"""Functions for processing and parsing Fluka files."""
import os.path

import antlr4

from .FlukaLexer import FlukaLexer
from .FlukaParser import FlukaParser

def Parse(path):
    """Return the antlr4 syntax tree for the given file."""
    if not os.path.exists(path):
        raise IOError("File not found: %s" % path)

    with open(path, 'r') as fluka_file:
        lines = fluka_file.readlines()

    _, geometry = _separate_geometry(lines)

    # Create ANTLR4 char stream from processed model string
    # geometry is a list of strings here, so join as single string.
    istream = antlr4.InputStream(''.join(geometry))

    # Tokenise character stream
    lexed_input = FlukaLexer(istream)

    # Create a buffer of tokens from lexer
    tokens = antlr4.CommonTokenStream(lexed_input)

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

    body_types = ["ARB", "BOX", "ELL", "PLA", "QUA", "RAW",
                  "RCC", "REC", "RPP", "SPH", "TRC", "WED",
                  "XCC", "XEC", "XYP", "XZP", "YCC", "YEC",
                  "YZP", "ZCC", "ZEC"]
    # Check if line after geobegin is a body definition, if not then
    # it is part of the GEOBEGIN card, and move begin_index onwards one.
    for body_type in body_types:
        if lines[geo_begin_index + 1].startswith(body_type):
            break
    else: # no break
        geo_begin_index += 1

    # Split the model into 3 parts
    before_geometry = lines[:geo_begin_index + 1]
    geometry = lines[geo_begin_index + 1:geo_end_index]
    after_geometry = lines[geo_end_index:]

    # Create list of equal length of commented lines to preserve line numbers
    commented_before_geometry = len(before_geometry) * ["*\n"]
    commented_geometry = len(geometry) * ["*\n"]
    commented_after_geometry = len(after_geometry) * ["*\n"]
    # Assemble and return the two sets:
    geometry = commented_before_geometry + geometry + commented_after_geometry
    not_geometry = before_geometry + commented_geometry + after_geometry

    return not_geometry, geometry
