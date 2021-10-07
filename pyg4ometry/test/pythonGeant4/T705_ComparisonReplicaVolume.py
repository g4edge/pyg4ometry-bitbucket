import os as _os
import pyg4ometry
import pyg4ometry.geant4 as _g4

def Test():
    r = _g4.Registry()

    tests = pyg4ometry.geant4.compare.Tests()
    
    galactic1 = _g4.MaterialPredefined("G4_Galactic", r)
    galactic2 = _g4.MaterialPredefined("G4_Galactic", r)

    # predefined materials
    comp1 = pyg4ometry.geant4.compare.materials(galactic1, galactic2, tests)
    comp1.Print()
    assert(len(comp1) == 0)
    
    return {"testStatus": True}

if __name__ == "__main__":
    Test()
