#!/bin/sh

coverage-2.7 run --source pyg4ometry --omit="*fluka*","*test*","*pygeometry*" ../pyg4ometry/test/runTests.py
coverage-2.7 report -m > runCoverage.log