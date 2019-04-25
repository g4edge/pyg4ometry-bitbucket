import unittest as _unittest

import pyg4ometry
import logging as _log

class PythonDefineTests(_unittest.TestCase) :

    def testConstantOperatorAddExpressionExpression(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1",r)
        yc = pyg4ometry.gdml.Constant("yc","2",r)
        self.assertEqual((xc+yc).eval(),3)

    def testConstantOperatorAddExpressionFloat(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1",r)
        self.assertEqual((xc+10).eval(),11)

    def testConstantOperatorAddFloatExpression(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1",r)
        self.assertEqual((10+xc).eval(),11)

    def testConstantOperatorSubExpressionExpression(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1",r)
        yc = pyg4ometry.gdml.Constant("yc","2",r)
        self.assertEqual((xc-yc).eval(),-1)

    def testConstantOperatorSubExpressionFloat(self) : 
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1",r)
        self.assertEqual((xc-10).eval(),-9)

    def testConstantOperatorSubExpressionFloat(self) : 
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1",r)
        self.assertEqual((10-xc).eval(),9)

    def testConstantOperatorMulExpressionExpression(self) : 
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","5",r)
        yc = pyg4ometry.gdml.Constant("yc","5",r)
        self.assertEqual((xc*yc).eval(),25)

    def testConstantOperatorMulExpressionFloat(self) : 
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","5",r)
        self.assertEqual((xc*5).eval(),25)

    def testConstantOperatorMulFloatExpression(self) : 
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","5",r)
        self.assertEqual((5*xc).eval(),25)
                
    def testConstantOperatorDivExpressionExpression(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","5",r)
        yc = pyg4ometry.gdml.Constant("yc","10",r)
        self.assertEqual((xc/yc).eval(),0.5)        

    def testConstantOperatorDivExpressionFloat(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","5",r)
        self.assertEqual((xc/10).eval(),0.5)        

    def testConstantOperatorDivFloatExpression(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","5",r)
        self.assertEqual((10./xc).eval(),2)        

    def testConstantOperationNegExpression(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","5",r)
        self.assertEqual((-xc).eval(),-5)                

    def testConstantSinExpression(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","0.1",r)
        self.assertEqual((pyg4ometry.gdml.sin(xc)).eval(),0.09983341664682815)

    def testConstantCosExpression(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","0.1",r)
        self.assertEqual((pyg4ometry.gdml.cos(xc)).eval(),0.9950041652780257) 

    def testConstantTanExpression(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","0.1",r)
        self.assertEqual((pyg4ometry.gdml.tan(xc)).eval(),0.10033467208545055) 

#    def testConstantExpExpression(self) :
#        r = pyg4ometry.geant4.Registry()
#        xc = pyg4ometry.gdml.Constant("xc","0.1",r)
#        self.assertEqual((pyg4ometry.gdml.exp(xc)).eval(),1.1051709180756477) 

    def testConstantLogExpression(self) : 
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","0.1",r)
        self.assertEqual((pyg4ometry.gdml.log(xc)).eval(),-2.3025850929940455) 

#    def testConstantLog10Expression(self) : 
#        r = pyg4ometry.geant4.Registry()
#        xc = pyg4ometry.gdml.Constant("xc","0.1",r)
#        self.assertEqual((pyg4ometry.gdml.log10(xc)).eval(),-0.1) 

    def testConstantSqrtExpression(self) : 
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","0.1",r)
        self.assertEqual((pyg4ometry.gdml.sqrt(xc)).eval(),0.31622776601683794) 

    def testConstantArcSinExpression(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","0.1",r)
        self.assertEqual((pyg4ometry.gdml.asin(xc)).eval(),0.1001674211615598)

    def testConstantArcCosExpression(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","0.1",r)
        self.assertEqual((pyg4ometry.gdml.acos(xc)).eval(),1.4706289056333368) 

    def testConstantArcTanExpression(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","0.1",r)
        self.assertEqual((pyg4ometry.gdml.atan(xc)).eval(),0.09966865249116204) 

if __name__ == '__main__':
    _unittest.main(verbosity=2)        
