import pyg4ometry

def DefinesTest() : 
    print('DefinesTest> Registry')
    r = pyg4ometry.geant4.Registry()

    print('DefinesTest> Constant construction')
    x = pyg4ometry.gdml.Constant("x","1",r)
    y = pyg4ometry.gdml.Constant("y","2",r)
    z = pyg4ometry.gdml.Constant("z","3",r)
    print(x)
    print(y)
    print(z)

    print('DefinesTest> Constant binary operations')
    v001  = x+y
    v002  = x+10
    v003  = 10+x 
    v004  = x-y
    v005  = x-10
    v006  = 10-x
    v007  = x*y
    v008  = 10*x
    v009  = x*10
    v010  = x/y
    v011  = x/10
    v012  = -x
    
    print(v001, v001.eval(), v001.eval() ==  3)
    print(v002, v002.eval(), v002.eval() == 11)
    print(v003, v003.eval(), v003.eval() == 11)
    print(v004, v004.eval(), v004.eval() == -1)
    print(v005, v005.eval(), v005.eval() == -9)
    print(v006, v006.eval(), v006.eval() == -9)
    print(v007, v007.eval(), v007.eval() ==  2)
    print(v008, v008.eval(), v008.eval() == 10)
    print(v009, v009.eval(), v009.eval() == 10)
    print(v010, v010.eval(), v010.eval() == 0.5)
    print(v011, v011.eval(), v011.eval() == 0.1)
    print(v012, v012.eval(), v012.eval() == -1)


    print('DefinesTest> Constant functions')
        

    print('DefinesTest> position construction')
    p001 = pyg4ometry.gdml.Position("p001",x,y,z,"mm",r)
    p002 = pyg4ometry.gdml.Position("p002","1",y,z,"mm",r)
    p003 = pyg4ometry.gdml.Position("p003",x,"2",z,"mm",r)
    p004 = pyg4ometry.gdml.Position("p004",x,y,"3","mm",r)
    p005 = pyg4ometry.gdml.Position("p005",v001,y,z,"mm",r)
    p006 = pyg4ometry.gdml.Position("p006",x,v001,z,"mm",r)
    p007 = pyg4ometry.gdml.Position("p007",x,y,v001,"mm",r)

    print(p001, p001.eval())
    print(p002, p002.eval())
    print(p003, p003.eval())
    print(p004, p004.eval())
    print(p005, p005.eval())
    print(p006, p006.eval())
    print(p007, p007.eval())

    print('DefinesTest> position binary operations')
    print(p001+p005, (p001+p005).eval())
    print(p001-p005, (p001-p005).eval())
    print(p001*10,   (p001*10).eval())
    print(p001*y,    (p001*y).eval())
    print(10*p001,   (p001*10).eval())
    print(y*p001,    (y*p001).eval())
    print(p001/10,   (p001/10).eval())
    print(p001/y,    (p001/y).eval())
    
    return r
