import pyg4ometry
import pyg4ometry.geant4 as _g4

def Test():
    r = _g4.Registry()

    tests = pyg4ometry.compare.Tests()
    
    galactic1 = _g4.MaterialPredefined("G4_Galactic", r)
    galactic2 = _g4.MaterialPredefined("G4_Galactic", r)

    # predefined materials
    comp1 = pyg4ometry.compare.materials(galactic1, galactic2, tests)
    comp1.Print()
    assert(len(comp1) == 0)

    # different predefined
    iron = _g4.MaterialPredefined("G4_Fe", r)
    comp2 = pyg4ometry.compare.materials(galactic1, iron, tests)
    comp2.Print()
    assert(len(comp2) > 0)

    # predefined vs single element
    iron2 = _g4.MaterialSingleElement("iron",26,55.8452,7.874,r) # iron at near room temp
    comp3 = pyg4ometry.compare.materials(galactic1, iron2, tests)
    comp3.Print()
    assert(len(comp3) > 0)

    # single element material with itself
    comp4 = pyg4ometry.compare.materials(iron2, iron2, tests)
    comp4.Print()
    assert(len(comp4) == 0)

    # material of elements with mass fraction
    air = _g4.MaterialCompound("air",1.290e-3,2,r)
    ne = _g4.ElementSimple("nitrogen","N",7,14.01,r)
    oe = _g4.ElementSimple("oxygen","O",8,16.0,r)
    air.add_element_massfraction(ne,0.7)
    air.add_element_massfraction(oe,0.3)
    comp5 = pyg4ometry.compare.materials(air, air, tests)
    comp5.Print()
    assert(len(comp5) == 0)

    comp6 = pyg4ometry.compare.materials(air, iron2, tests)
    comp6.Print()
    assert(len(comp6) > 0)

    # different density
    air2= _g4.MaterialCompound("air", 1.291e-3, 2, r)
    air2.add_element_massfraction(ne, 0.7)
    air2.add_element_massfraction(oe, 0.3)
    comp7 = pyg4ometry.compare.materials(air, air2, tests)
    comp7.Print()
    assert (len(comp7) > 0)

    # different mass fraction
    air3 = _g4.MaterialCompound("air", 1.291e-3, 2, r)
    air3.add_element_massfraction(ne, 0.701)
    air3.add_element_massfraction(oe, 0.299)
    comp8 = pyg4ometry.compare.materials(air2, air3, tests)
    comp8.Print()
    assert (len(comp8) > 0)

    # different n components
    air4 = _g4.MaterialCompound("air4", 1.291e-3, 3, r)
    air4.add_element_massfraction(ne, 0.700)
    air4.add_element_massfraction(oe, 0.299)
    are = _g4.ElementSimple("argon", "Ar", 18, 40.0, r)
    air4.add_element_massfraction(are, 0.001)

    comp9 = pyg4ometry.compare.materials(air3, air4, tests)
    comp9.Print()
    assert (len(comp9) > 0)

    water = _g4.MaterialCompound("water", 1.0, 2, r)
    he = _g4.ElementSimple("hydrogen", "H", 1, 1.01)
    oe = _g4.ElementSimple("oxygen", "O", 8, 16.0)
    water.add_element_natoms(he, 2)
    water.add_element_natoms(oe, 1)

    # n atoms no difference
    comp10 = pyg4ometry.compare.materials(water, water, tests)
    comp10.Print()
    assert (len(comp10) == 0)

    # n atoms type vs fractional mass type - can't compare
    comp11 = pyg4ometry.compare.materials(air3, water, tests)
    comp11.Print()
    assert (len(comp11) > 0)

    tests2 = pyg4ometry.compare.Tests()
    tests2.materialCompositionType = False
    comp11b = pyg4ometry.compare.materials(air3, water, tests2)
    comp11b.Print()
    assert (len(comp11) > 0)

    # n atoms difference
    water2 = _g4.MaterialCompound("water", 1.0, 2, r)
    water2.add_element_natoms(he, 3)
    water2.add_element_natoms(oe, 1)
    comp12 = pyg4ometry.geant4.materials(water, water2, tests)
    comp12.Print()
    assert (len(comp12) > 0)

    return {"testStatus": True}

if __name__ == "__main__":
    Test()
