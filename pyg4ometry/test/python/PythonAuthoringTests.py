import unittest as _unittest

import T001_Box
import logging as _log

logger = _log.getLogger()
logger.disabled = True

class PythonAuthoringTests(_unittest.TestCase) :
    def testBox(self) :
        self.assertTrue(T001_Box.Test())

#    def testCons(self) :
#        self.assertEqual(T002_Cons.Test(), True)

if __name__ == '__main__':
    _unittest.main(verbosity=2)        
