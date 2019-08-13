import unittest as _unittest

import pyg4ometry
import logging as _log

class PythonDefineTests(_unittest.TestCase) :

    # #############################
    # Define upgrades
    # #############################
    def testUpgradeToStringExpression(self) :
        r = pyg4ometry.geant4.Registry()

        # number to expression string
        self.assertEqual(pyg4ometry.gdml.upgradeToStringExpression(r,10),"10.000000000000000")

        # string to expression string (evaluatable)
        self.assertEqual(pyg4ometry.gdml.upgradeToStringExpression(r,"10+10"),"10+10")

        # string to expression string (unevaluatable)

        x = pyg4ometry.gdml.Constant("x", 1, r)

        try : 
            self.assertEqual(pyg4ometry.gdml.upgradeToStringExpression(r,"10*x+10"),"10*x+10")
        except AttributeError : 
            pass

        # string but in define dict 
        c = pyg4ometry.gdml.Defines.Constant("c","10",r,True)
        self.assertEqual(pyg4ometry.gdml.upgradeToStringExpression(r,"c"),"c")

    def testUpgradeToVector(self) : 
        r = pyg4ometry.geant4.Registry() 

        v = pyg4ometry.gdml.Defines.Position("v",0,0,0,"mm",r,False)

        # vector 
        p = pyg4ometry.gdml.Defines.upgradeToVector(v,r,"position",False)
        self.assertEqual(p.eval(),[0,0,0])

        # list to position
        p = pyg4ometry.gdml.Defines.upgradeToVector([0,0,0],r,"position",False)
        self.assertEqual(p.eval(),[0,0,0])

        # list to rotation
        p = pyg4ometry.gdml.Defines.upgradeToVector([0,0,0],r,"rotation",False)
        self.assertEqual(p.eval(),[0,0,0])        

        # list to scale
        p = pyg4ometry.gdml.Defines.upgradeToVector([0,0,0],r,"scale",False)
        self.assertEqual(p.eval(),[0,0,0])

        # list to undefined
        p = pyg4ometry.gdml.Defines.upgradeToVector([0,0,0],r,"undefined",False)
        self.assertEqual(p,None)

        
    # #############################
    # ANTLR expressions 
    # #############################

    def testExpressionInt(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc",1,r)        
        self.assertEqual(xc.eval(),1)

    def testExpressionFloat(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc",1.2345,r)        
        self.assertEqual(xc.eval(),1.2345)

    def testExpressionScientific1(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc",1E3,r)        
        self.assertEqual(xc.eval(),1000)

    def testExpressionScientific2(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc",1.2345E3,r)
        self.assertEqual(xc.eval(),1234.5)

    def testExpressionStringInt(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1",r)        
        self.assertEqual(xc.eval(),1)

    def testExpressionStringFloat(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1.2345",r)        
        self.assertEqual(xc.eval(),1.2345)

    def testExpressionStringScientific1(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","1E3",r)        
        self.assertEqual(xc.eval(),1000)

    def testExpressionStringScientific2(self) :
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
    def testConstantSetName(self) : 
        r = pyg4ometry.geant4.Registry()
        c = pyg4ometry.gdml.Constant("xc","1",r)
        c.setName("testName") 
        self.assertEqual(c.name,"testName")
        self.assertEqual(c.expr.name,"expr_testName")
        
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

    def testPowExpression(self) :
        r = pyg4ometry.geant4.Registry()
        xc = pyg4ometry.gdml.Constant("xc","2",r)
        self.assertEqual((pyg4ometry.gdml.pow(xc,2)).eval(),4) 

    # #############################
    # Quantity
    # #############################        
    def testQuantity(self) : 
        r = pyg4ometry.geant4.Registry()
        xq = pyg4ometry.gdml.Quantity("xq","0.1","mass","kg",r)
        self.assertEqual(xq.eval(),0.1)
        self.assertEqual(float(xq),0.1)
        str(xq)

    # #############################
    # Variable
    # #############################        
    def testVariable(self) : 
        r = pyg4ometry.geant4.Registry()
        xv = pyg4ometry.gdml.Variable("xv","0.1",r)
        self.assertEqual(xv.eval(), 0.1)
        self.assertEqual(float(xv),0.1)
        str(xv)

    # #############################
    # Expression
    # #############################        
    def testExpression(self) : 
        r  = pyg4ometry.geant4.Registry()
        xe = pyg4ometry.gdml.Expression("xe","0.1",r,True)
        self.assertEqual(xe.eval(), 0.1)
        self.assertEqual(float(xe),0.1)
        str(xe)


    # #############################
    # Position
    # #############################                
    def testPositionSetName(self) :
        r = pyg4ometry.geant4.Registry()
        v = pyg4ometry.gdml.Position("p","1","2","3","mm",r)
        v.setName("newName")
        self.assertEqual(v.name,"newName")

    def testPositionGetItem(self) :
        r = pyg4ometry.geant4.Registry()
        v = pyg4ometry.gdml.Position("p","1","2","3","mm",r)

        self.assertEqual(v[0].eval(),1)
        self.assertEqual(v[1].eval(),2)
        self.assertEqual(v[2].eval(),3)
        
        try :
            v[3] 
        except IndexError : 
            pass 
        
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

    def testPositionConstructorUnitNone(self) :
        r = pyg4ometry.geant4.Registry()
        v = pyg4ometry.gdml.Position("p","1","2","3",None,r)
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
    def testRotation(self) : 
        r  = pyg4ometry.geant4.Registry()
        r1 = pyg4ometry.gdml.Rotation("r1",1,2,3,"rad",r,True)    
        r2 = pyg4ometry.gdml.Rotation("r2",1,2,3,"deg",r,True)
        r3 = pyg4ometry.gdml.Rotation("r3",1,2,3,None,r,True)
        r4 = pyg4ometry.gdml.Rotation("r4",1,2,3,None,r,False)
        str(r1)

    # #############################
    # Scale
    # #############################
    def testScale(self) : 
        r  = pyg4ometry.geant4.Registry()
        s1 = pyg4ometry.gdml.Scale("s1",1,2,3,None,r,True)    
        s2 = pyg4ometry.gdml.Scale("s2",1,2,3,None,r,False)    
        str(s1)

    # #############################
    # Matrix
    # #############################
    def testMatrixConstructor1x10(self) : 
        r = pyg4ometry.geant4.Registry()
        mat = pyg4ometry.gdml.Matrix("mat",1,[1,2,3,4,5,6,7,8,9,10],r,False)
        self.assertTrue((mat.eval() == [1,2,3,4,5,6,7,8,9,10]).all())

    def testMatrixConstructor1x10(self) : 
        r = pyg4ometry.geant4.Registry()
        mat = pyg4ometry.gdml.Matrix("mat",2,[1,2,3,4,5,6,7,8,9,10],r,False)

    def testMatrix1x10Index(self) : 
        r = pyg4ometry.geant4.Registry()
        mat = pyg4ometry.gdml.Matrix("mat",1,[1,2,3,4,5,6,7,8,9,10],r,False)
        self.assertEqual(mat[9].eval(),10)

    def testMatrix2x5Index(self) : 
        r = pyg4ometry.geant4.Registry()
        mat = pyg4ometry.gdml.Matrix("mat",2,[1,2,3,4,5,6,7,8,9,10],r,False)
        self.assertEqual(mat[0][2].eval(),3)

    def testMatrixConstructor1x10AddRegistry(self) : 
        r = pyg4ometry.geant4.Registry()
        mat = pyg4ometry.gdml.Matrix("mat",1,[1,2,3,4,5,6,7,8,9,10],r,True)
        self.assertTrue((mat.eval() == [1,2,3,4,5,6,7,8,9,10]).all())

    def testMatrixRepr(self) :
        r = pyg4ometry.geant4.Registry()
        mat = pyg4ometry.gdml.Matrix("mat",2,[1,2,3,4,5,6,7,8,9,10],r,True)
        str(mat)

    def testMatrixGetItemInRegistry(self) :
        r = pyg4ometry.geant4.Registry()
        mat = pyg4ometry.gdml.Matrix("mat",2,[1,2,3,4,5,6,7,8,9,10],r,True)
        self.assertEqual(mat[0,0].expr.expression,"mat[1,1]")
    
if __name__ == '__main__':
    _unittest.main(verbosity=2)        
        
