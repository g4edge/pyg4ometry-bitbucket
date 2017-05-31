import subprocess as _sp
import os.path as _path
import antlr4 as _antlr4

from FlukaLexer import FlukaLexer
from FlukaParser import FlukaParser

def Parse(path):
    if not _path.exists(path):
        raise IOError("File not found: %s" % path)

    with open(path, 'r') as f:
        file_string = f.read()

    # Create _ANTLR4 char stream from processed model string
    istream = _antlr4.InputStream(file_string)

    # Tokenise character stream
    lexed_input = FlukaLexer(istream)

    # Create a buffer of tokens from lexer
    tokens = _antlr4.CommonTokenStream(lexed_input)

    # Create a parser that reads from stream of tokens
    parser = FlukaParser(tokens)

    # Create syntax tree
    tree = parser.model()

    return tree


def VisitModel(tree):

    if visitor != default:
        pass

    visitor = FlukaTreeVisitor()
