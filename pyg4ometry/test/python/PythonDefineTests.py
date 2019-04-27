import unittest as _unittest

import pyg4ometry
import logging as _log

class PythonDefineTests(_unittest.TestCase) :

    # #############################
    # ANTLR expressions 
    # #############################

    def testExpressionInt(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1",r)        
        self.assertEqual(xc.eval(),1)

    def testExpressionFloat(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1.2345",r)        
        self.assertEqual(xc.eval(),1.2345)


    def testExpressionIntScientific(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1E3",r)        
        self.assertEqual(xc.eval(),1000)

    def testExpressionFloatScientific(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1.2345E3",r)
        self.assertEqual(xc.eval(),1234.5)

    def testExpressionOperatorAddIntInt(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1+2",r)        
        self.assertEqual(xc.eval(),3)        

    def testExpressionOperatorAddIntFloat(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","2.3456+1",r)
        self.assertEqual(xc.eval(),3.3456)        

    def testExpressionOperatorAddFloatFloat(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1.2345+2.3456",r)
        self.assertEqual(xc.eval(),3.5801)        

    def testExpressionOperatorAddFloatInt(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1+2.3456",r)
        self.assertEqual(xc.eval(),3.3456)        

    def testExpressionOperatorSubIntInt(self) : 
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1-2",r)        
        self.assertEqual(xc.eval(),-1)                

    def testExpressionOperatorSubIntFloat(self) : 
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1-2.3456",r)
        self.assertEqual(xc.eval(),-1.3456000000000001)

    def testExpressionOperatorSubFloatInt(self) : 
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","2.3456-1",r)
        self.assertEqual(xc.eval(),1.3456000000000001)

    # #############################
    # Constants 
    # #############################        
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

    def testConstantExpExpression(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","0.1",r)
        self.assertEqual((pyg4ometry.gdml.exp(xc)).eval(),1.1051709180756477) 

    def testConstantLogExpression(self) : 
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","0.1",r)
        self.assertEqual((pyg4ometry.gdml.log(xc)).eval(),-2.3025850929940455) 

    def testConstantLog10Expression(self) : 
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","0.1",r)
        self.assertEqual((pyg4ometry.gdml.log10(xc)).eval(),-1.0) 

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

    # #############################
    # Quanty
    # #############################        

    # #############################
    # Variable
    # #############################        

    # #############################
    # Position
    # #############################        
        
    def testPositionConstructorStrStrStr(self) :
        r = pyg4ometry.geant4.Registry()
        v = pyg4ometry.gdml.Position("p","1","2","3","mm",r)
        self.assertEqual(v.eval(),[1,2,3])

    def testPositionConstructorStrStrFloat(self) :
        r = pyg4ometry.geant4.Registry()
        v = pyg4ometry.gdml.Position("p","1","2",3,"mm",r)
        self.assertEqual(v.eval(),[1,2,3])

    def testPositionConstructorStrFloatStr(self) :
        r = pyg4ometry.geant4.Registry()
        v = pyg4ometry.gdml.Position("p","1",2,"3","mm",r)
        self.assertEqual(v.eval(),[1,2,3])

    def testPositionConstructorFloatStrStr(self) :
        r = pyg4ometry.geant4.Registry()
        v = pyg4ometry.gdml.Position("p",1,"2","3","mm",r)
        self.assertEqual(v.eval(),[1,2,3])

    def testPositionConstructorStrStrExpression(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","3",r)
        v = pyg4ometry.gdml.Position("p","1","2",xc,"mm",r)
        self.assertEqual(v.eval(),[1,2,3])

    def testPositionConstructorStrExpressionStr(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","2",r)
        v = pyg4ometry.gdml.Position("p","1",xc,"3","mm",r)
        self.assertEqual(v.eval(),[1,2,3])

    def testPositionConstructorExpressionStrStr(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1",r)
        v = pyg4ometry.gdml.Position("p",xc,"2","3","mm",r)
        self.assertEqual(v.eval(),[1,2,3])

    def testPositionConstructorStrStrExprstr(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","3",r)
        v = pyg4ometry.gdml.Position("p","1","2","xc","mm",r)
        self.assertEqual(v.eval(),[1,2,3])

    def testPositionConstructorStrExprstrStr(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","2",r)
        v = pyg4ometry.gdml.Position("p","1","xc","3","mm",r)
        self.assertEqual(v.eval(),[1,2,3])

    def testPositionConstructorExprstrStrStr(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1",r)
        v = pyg4ometry.gdml.Position("p","xc","2","3","mm",r)
        self.assertEqual(v.eval(),[1,2,3])

    def testPositionOperatorAdd(self) : 
        r = pyg4ometry.geant4.Registry()
        v1 = pyg4ometry.gdml.Position("v1","1","2","3","mm",r)
        v2 = pyg4ometry.gdml.Position("v2","11","12","13","mm",r)
        self.assertEqual((v1+v2).eval(),[12,14,16])        

    def testPositionOperatorSub(self) : 
        r = pyg4ometry.geant4.Registry()
        v1 = pyg4ometry.gdml.Position("v1","1","2","3","mm",r)
        v2 = pyg4ometry.gdml.Position("v2","11","12","13","mm",r)
        self.assertEqual((v2-v1).eval(),[10,10,10])        

    def testPositionOperatorMulFloatPosition(self) : 
        r = pyg4ometry.geant4.Registry()
        v1 = pyg4ometry.gdml.Position("v1","1","2","3","mm",r)
        self.assertEqual((10.*v1).eval(),[10,20,30])        

    def testPositionOperatorMulPositionFloat(self) : 
        r = pyg4ometry.geant4.Registry()
        v1 = pyg4ometry.gdml.Position("v1","1","2","3","mm",r)
        self.assertEqual((v1*10.).eval(),[10,20,30])        

    def testPositionOperatorMulExpressionPosition(self) : 
        r = pyg4ometry.geant4.Registry()
        x = pyg4ometry.gdml.Constant("x","1.5",r)
        v1 = pyg4ometry.gdml.Position("v1","1","2","3","mm",r)
        self.assertEqual((x*v1).eval(),[1.5,3.0,4.5])            

    def testPositionOperatorMulPositionExpression(self) : 
        r = pyg4ometry.geant4.Registry()
        x = pyg4ometry.gdml.Constant("x","1.5",r)
        v1 = pyg4ometry.gdml.Position("v1","1","2","3","mm",r)
        self.assertEqual((v1*x).eval(),[1.5,3.0,4.5])            

    def testPositionOperatorDivPositionFloat(self) : 
        r = pyg4ometry.geant4.Registry()
        v1 = pyg4ometry.gdml.Position("v1","1","2","3","mm",r)
        self.assertEqual((v1/10).eval(),[0.1,0.2,0.3])

    def testPositionOperatorDivPositionExpression(self) : 
        r = pyg4ometry.geant4.Registry()
        x = pyg4ometry.gdml.Constant("x","10.0",r)
        v1 = pyg4ometry.gdml.Position("v1","1","2","3","mm",r)
        self.assertEqual((v1/x).eval(),[0.1,0.2,0.3])

    # #############################
    # Rotations
    # #############################

    # #############################
    # Scale
    # #############################

    # #############################
    # Matrix
    # #############################
    
if __name__ == '__main__':
    _unittest.main(verbosity=2)        
        
