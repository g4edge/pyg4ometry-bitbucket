import unittest as _unittest

import T001_Box
import T002_Tubs
import T003_CutTubs

import logging as _log

logger = _log.getLogger()
logger.disabled = True

class PythonAuthoringTests(_unittest.TestCase) :
    def testBox(self) :
        self.assertTrue(T001_Box.Test())

    def testTubs(self) :
        self.assertTrue(T002_Tubs.Test())

    def testCutTubs(self) :
        self.assertTrue(T003_CutTubs.Test())

if __name__ == '__main__':
    _unittest.main(verbosity=2)        
