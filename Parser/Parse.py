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

    lines = _remove_col0_comments(lines)
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
    tree = parser.model()

    return tree

def _remove_col0_comments(lines):
    # Loop over all lines and remove those that have an '*' in column
    # 0.  The other comment type is '!', which doesn't necessarily
    # have to be in column 0.
    for index, line in enumerate(lines):
        if line[0] == '*' or line[0] == '!':
            del lines[index]
    return lines

def _separate_geometry(lines):
    # Get the two indices of geobegin and geoend
    geo_begin_index = (i for i, line in enumerate(lines)
                       if line.startswith("GEOBEGIN")).next()
    geo_end_index = (i for i, line in enumerate(lines)
                     if line.startswith("GEOEND")).next()
    # slice and return
    before_geometry = lines[:geo_begin_index]
    geometry = lines[geo_begin_index:geo_end_index + 1]
    after_geometry = lines[geo_end_index + 1:]
    not_geometry = before_geometry + after_geometry

    return not_geometry, geometry

def VisitModel(tree):

    if visitor != default:
        pass

    visitor = FlukaTreeVisitor()
