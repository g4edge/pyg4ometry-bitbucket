#!/bin/sh


# 1150.988s 2019/10/27

coverage-3.7 run --source pyg4ometry --omit="*test*","*gui*","*RegionLexer*","*RegionParser*","*RegionParserVisitor*","*GdmlExpressionLexer*","*GdmlExpressionParser*","*GdmlExpressionParserVisitor*" runTests.py
coverage-3.7 report -m > runCoverage.log