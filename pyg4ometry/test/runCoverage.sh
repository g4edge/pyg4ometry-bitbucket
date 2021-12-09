#!/bin/sh


# 1150.988s 2019/10/27
COVCOMMAND=coverage-3.9
$COVCOMMAND run --source pyg4ometry --omit="*test*","*gui*","*RegionLexer*","*RegionParser*","*RegionParserVisitor*","*GdmlExpressionLexer*","*GdmlExpressionParser*","*GdmlExpressionParserVisitor*" runTests.py
$COVCOMMAND report -m > runCoverage.log
