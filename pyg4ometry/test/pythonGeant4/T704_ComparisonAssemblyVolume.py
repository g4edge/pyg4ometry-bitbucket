import pyg4ometry
import pyg4ometry.geant4 as _g4

def Test():
    r = _g4.Registry()

    # in all of these we force testsAlreadyDone=[] as an argument to reset
    # the one 'definition' of it in python. We have to be careful with this
    # trick for pass by reference-like arguments

    # we use successive new registries for a mish-mash of bits (not caring about writing out)
    # so we can have degenerate names - the comparison doesn't care - it just looks at parameters

    tests = pyg4ometry.compare.Tests()
    
    galactic1 = _g4.MaterialPredefined("G4_Galactic", r)
    galactic2 = _g4.MaterialPredefined("G4_Galactic", r)

    # predefined materials
    comp1 = pyg4ometry.compare.materials(galactic1, galactic2, tests)
    comp1.print()
    assert(len(comp1) == 0)

    # some geometry
    a_a_solid = _g4.solid.Box("a_a_solid", 50, 40, 30, r)
    a_b_solid = _g4.solid.Tubs("a_b_solid",0, 12, 30, 0, "2*pi", r)
    iron = _g4.MaterialPredefined("G4_Fe")
    copper = _g4.MaterialPredefined("G4_Cu")
    a_a_lv = _g4.LogicalVolume(a_a_solid, copper, "a_a_lv", r)
    a_b_lv = _g4.LogicalVolume(a_b_solid, copper, "a_b_lv", r)
    a_ass = _g4.AssemblyVolume("a_assembly", r)
    a_a_pv = _g4.PhysicalVolume([0,0,0], [0,0,100], a_a_lv, "a_a_pv1", a_ass, r)
    a_b_pv = _g4.PhysicalVolume([0,0,0], [0,0,50],  a_b_lv, "a_b_pv1", a_ass, r)

    # with itself
    comp2 = pyg4ometry.compare.assemblyVolumes(a_ass, a_ass, tests, testsAlreadyDone=[])
    comp2.print()
    assert(len(comp2) == 0)

    # missing daughter
    r2 = _g4.Registry()
    b_ass = _g4.AssemblyVolume("a_assembly", r2)
    b_a_pv = _g4.PhysicalVolume([0,0,0], [0,0,100], a_a_lv, "a_a_pv1", b_ass, r2)
    comp3 = pyg4ometry.compare.assemblyVolumes(a_ass, b_ass, tests, testsAlreadyDone=[])
    comp3.print()
    assert(len(comp3) == 1)

    # extra daughter
    r3 = _g4.Registry()
    c_ass = _g4.AssemblyVolume("a_assembly", r3)
    c_a_pv  = _g4.PhysicalVolume([0,0,0], [0,0,100], a_a_lv, "a_a_pv1", c_ass, r3)
    c_b1_pv = _g4.PhysicalVolume([0,0,0], [0,0,50],  a_b_lv, "a_b_pv1", c_ass, r3)
    c_b2_pv = _g4.PhysicalVolume([0,0,0], [0,0,0],   a_b_lv, "a_b_pv2", c_ass, r3)
    comp4 = pyg4ometry.compare.assemblyVolumes(a_ass, c_ass, tests, testsAlreadyDone=[])
    comp4.print()
    assert(len(comp4) == 1)

    # different daughter by name
    r4 = _g4.Registry()
    d_ass = _g4.AssemblyVolume("a_assembly", r4)
    d_a_pv = _g4.PhysicalVolume([0,0,0], [0,0,100], a_a_lv, "a_aaaa_pv1", d_ass, r4)
    d_b_pv = _g4.PhysicalVolume([0,0,0], [0,0,50],  a_b_lv, "a_b_pv1", d_ass, r4)
    comp5 = pyg4ometry.compare.assemblyVolumes(a_ass, d_ass, tests, testsAlreadyDone=[])
    comp5.print()
    assert(len(comp5) == 2) # both missing and extra

    # different values of pvs
    r5 = _g4.Registry()
    e_ass = _g4.AssemblyVolume("a_assembly", r5)
    e_a_pv = _g4.PhysicalVolume([0, 0, 0], [0, 0, -100], a_a_lv, "a_a_pv1", e_ass, r5)
    e_b_pv = _g4.PhysicalVolume([0, 0, 0], [0, 0, 50], a_b_lv, "a_b_pv1", e_ass, r5)
    comp6 = pyg4ometry.compare.assemblyVolumes(a_ass, e_ass, tests, testsAlreadyDone=[])
    comp6.print()
    assert (len(comp6) == 1)

    # different values of lv material inside pvs inside avs
    r6 = _g4.Registry()
    f_ass = _g4.AssemblyVolume("a_assembly", r6)
    a_b_lv = _g4.LogicalVolume(a_b_solid, iron, "a_b_lv", r6)
    f_a_pv = _g4.PhysicalVolume([0, 0, 0], [0, 0, 100], a_a_lv, "a_a_pv1", f_ass, r6)
    f_b_pv = _g4.PhysicalVolume([0, 0, 0], [0, 0, 50], a_b_lv, "a_b_pv1", f_ass, r6)
    comp7 = pyg4ometry.compare.assemblyVolumes(a_ass, f_ass, tests, testsAlreadyDone=[])
    comp7.print()
    assert (len(comp7) == 1)

    return {"testStatus": True}

if __name__ == "__main__":
    Test()
