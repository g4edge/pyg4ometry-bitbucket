import subprocess as _sp

import antlr4 as _antlr4

from FlukaLexer import FlukaLexer
from FlukaParser import FlukaParser

def PreProcessFile(filein):
    # Can use cpp preprocessor with a bit of  prepreprocessing.
    p1 = _sp.Popen(['sed', 's/^#if/& defined/g', filein], stdout=_sp.PIPE)
    p2 = _sp.Popen(['sed', 's/^#elif/& defined/g'], stdin=p1.stdout,
                   stdout=_sp.PIPE)
    p1.stdout.close()
    p3 = _sp.Popen(['cpp', '-E' , '-P'], stdin=p2.stdout, stdout=_sp.PIPE)

    processed_model_string = p3.stdout.read()

    return processed_model_string

def Parse(input):

    # Preprocess input:
    processed_string = PreProcessFile(input)

    # Create _ANTLR4 char stream from processed model string
    istream = _antlr4.InputStream(processed_string)

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
