#!/bin/sh


# 1150.988s 2019/10/27

coverage-2.7 run --source pyg4ometry --omit="*test*","*gui*" ../pyg4ometry/test/runTests.py
coverage-2.7 report -m > runCoverage.log