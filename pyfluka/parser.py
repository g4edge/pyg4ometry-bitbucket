"""Functions for processing and parsing Fluka files."""
import os.path
import collections
import warnings

import antlr4

import pyfluka.FlukaLexer
import pyfluka.FlukaParser


def get_geometry_ast_and_other_cards(path):
    """Return the antlr4 syntax tree for the given file."""
    if not os.path.exists(path):
        raise IOError("File not found: %s" % path)

    with open(path, 'r') as fluka_file:
        lines = fluka_file.readlines()

    not_geometry, geometry = _separate_geometry(lines)

    # Create ANTLR4 char stream from processed model string
    # geometry is a list of strings here, so join as single string.
    istream = antlr4.InputStream(''.join(geometry))

    # Tokenise character stream
    lexed_input = pyfluka.FlukaLexer.FlukaLexer(istream)

    # Create a buffer of tokens from lexer
    tokens = antlr4.CommonTokenStream(lexed_input)

    # Create a parser that reads from stream of tokens
    parser = pyfluka.FlukaParser.FlukaParser(tokens)

    # Create syntax tree
    tree = parser.geocards()

    # Blindly assume all lines in not_geometry are of fixed format.  Will be OK
    # for now.
    not_geometry = map(Card.from_fixed_line, not_geometry)
    return tree, not_geometry


def _separate_geometry(lines):
    """Separate the model into two parts, lines describing the
    geometry, and lines describing what is not the geometry.  In both
    cases, the other is commented out rather than removed.  This is
    useful as the line numbering is retained.

    """
    # Get the two indices of geobegin and geoend
    try:
        geo_begin_index = (i for i, line in enumerate(lines)
                           if line.startswith("GEOBEGIN")).next()
        geo_end_index = (i for i, line in enumerate(lines)
                         if line.startswith("GEOEND")).next()
    except StopIteration:
        msg = "GEOBEGIN and/or GEOEND cards not found and/or malformed!"
        raise IOError(msg)

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
    commented_after_geometry = len(after_geometry) * ["*\n"]
    # Assemble and return the two sets:
    geometry = commented_before_geometry + geometry + commented_after_geometry
    not_geometry = before_geometry + after_geometry

    return _strip_comments(not_geometry), geometry


def _strip_comments(lines):
    return [line for line in lines if not line.startswith('*')]

class Card(collections.namedtuple("Card",
                                  ["keyword", "what1", "what2", "what3",
                                   "what4", "what5", "what6", "sdum"])):

    @classmethod
    def from_fixed_line(cls, line):
        # Don't know if this is actually necessary but just in case..
        if len(line) > 80:
            raise TypeError("Line too long!  Maximum line length is 80.")
        line = line.rstrip('\n')
        # column positions are multiples of 10 up to 80 inclusive.
        positions = [10 * x for x in range(9)]
        # Split the line into a list of strings according to the positions
        columns = [line[start:stop]
                   for start, stop in zip(positions, positions[1:])]
        # remove trailing/leading whitepace
        columns = [column.strip() for column in columns]
        # Empty strings -> None
        columns = [column if column != "" else None for column in columns]
        columns = [Card._attempt_float_coercion(column) for column in columns]
        return cls(*columns)

    @classmethod
    def from_free_line(cls, line, sep=None):
        pass

    def warn_not_supported(self, supported_fields):
        """User provides an iterable of SUPPORTED fields of the form
        ["what1", "what2", "sdum"], and warnings will be raised once if
        there are any fields which are not None which do not feature in fields.

        """
        for field in self._fields:
            if (getattr(self, field) is not None
                    and field not in supported_fields):
                warnings.simplefilter('once', UserWarning)
                msg = ("{} not supported for card \"{}\"."
                       "  This field will be ignored.".format(field.upper(),
                                                               self.keyword))
                warnings.warn(msg)

    @staticmethod
    def _attempt_float_coercion(string):
        try:
            return float(string)
        # (Not a coercable string, not a coercable type)
        except (ValueError, TypeError):
            return string
