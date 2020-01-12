#!/bin/sh


# 1150.988s 2019/10/27

coverage-2.7 run --source pyg4ometry --omit="*test*","*gui*","*RegionLexer*","*RegionParser*","*RegionParserVisitor*","*GdmlExpressionLexer*","*GdmlExpressionParser*","*GdmlExpressionParserVisitor*" ../pyg4ometry/test/runTests.py
coverage-2.7 report -m > runCoverage.log