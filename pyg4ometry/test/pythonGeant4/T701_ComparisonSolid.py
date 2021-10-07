import os as _os
import pyg4ometry
import pyg4ometry.geant4 as _g4

def Test():
    r = _g4.Registry()

    tests = pyg4ometry.geant4.Compare.Tests()

    box1 = _g4.solid.Box("box1", 100, 80, 60, r)
    
    # solid with itself
    comp1 = pyg4ometry.geant4.Compare.solids(box1, box1, tests)
    comp1.Print()
    assert(len(comp1) == 0)

    wx = pyg4ometry.gdml.Constant("wx", 100, r)
    box2 = _g4.solid.Box("box2", "1*wx", 0.8*wx, 0.6*wx, r)

    # solid with itself - using expressions
    comp2 = pyg4ometry.geant4.Compare.solids(box2, box2, tests)
    comp2.Print()
    assert(len(comp2) == 0)

    # box with numbers vs box with expressions but equivalent
    # only name should be different
    comp3 = pyg4ometry.geant4.Compare.solids(box1, box2, tests)
    comp3.Print()
    assert(len(comp3) == 1)

    testsNoName = pyg4ometry.geant4.Compare.Tests()
    testsNoName.names = False
    comp4 = pyg4ometry.geant4.Compare.solids(box1, box2, testsNoName, "maintest", includeAllTestResults=True)
    comp4.Print()
    assert (len(comp4) > 0) # because we include all tests

    # test a solid where a parameter is potentially a list or not just a number
    p1x = pyg4ometry.gdml.Constant("p1x", "-20", r, True)
    p1y = pyg4ometry.gdml.Constant("p1y", "-20", r, True)
    z1, x1, y1, s1 = -20,  5,  5, 1
    z2, x2, y2, s2 =   0, -5, -5, 1
    z3, x3, y3, s3 =  20,  0,  0, 2
    polygon = [[p1x, p1y], [-20, 20], [20, 20], [20, 10], [-10, 10], [-10, 10], [20, -10], [20, -20]]
    slices = [[z1, [x1, y1], s1], [z2, [x2, y2], s2], [z3, [x3, y3], s3]]
    xs = _g4.solid.ExtrudedSolid("xs", polygon, slices, r)

    # complex solid with other with simple values
    comp5 = pyg4ometry.geant4.Compare.solids(box1, xs, tests)
    comp5.Print()
    assert (len(comp5) > 0)

    comp6 = pyg4ometry.geant4.Compare.solids(xs, xs, tests)
    comp6.Print()
    assert (len(comp6) == 0)

    # one number deep inside that's slightly different
    polygon2 = [[p1x, p1y], [-20, 20], [30, 20], [20, 10], [-10, 10], [-10, 10], [20, -10], [20, -20]]
    slices2 = [[z1, [6, y1], s1], [z2, [x2, y2], s2], [z3, [x3, y3], s3]]
    xs2 = _g4.solid.ExtrudedSolid("xs2", polygon2, slices2, r)
    comp7 = pyg4ometry.geant4.Compare.solids(xs, xs2, tests)
    comp7.Print()
    assert (len(comp7) > 0)

    return {"testStatus": True}

if __name__ == "__main__":
    Test()
