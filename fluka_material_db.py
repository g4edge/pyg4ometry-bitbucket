"""Some constants useful for converting Fluka materials to GDML materials.

FLUKA_G4_MATERIAL_MAP maps Fluka Material names to their corresponding
Geant4 material names.

"""

# Dictionary for converting Fluka's built-in element and compound
# materials to Geant4 materials.  "None" doesn't guarantee that Geant4
# doesn't have them, I just didn't try too hard to match them except in the
# case of BLCKHOLE, which has no Geant4 analogue.
FLUKA_G4_MATERIAL_MAP = {"BLCKHOLE": None, # Shouldn't convert BLCKHOLE.
                         "VACUUM": "G4_Galactic",
                         "HYDROGEN": "G4_H",
                         "HELIUM": "G4_He",
                         "BERYLLIU": "G4_Be",
                         "CARBON": "G4_C",
                         "NITROGEN": "G4_N",
                         "OXYGEN": "G4_O",
                         "MAGNESIU": "G4_Mg",
                         "ALUMINUM": "G4_Al",
                         "IRON": "G4_Fe",
                         "COPPER": "G4_Cu",
                         "SILVER": "G4_Ag",
                         "SILICON": "G4_Si",
                         "GOLD": "G4_Au",
                         "MERCURY": "G4_Hg",
                         "LEAD": "G4_Pb",
                         "TANTALUM": "G4_Ta",
                         "SODIUM": "G4_Na",
                         "ARGON": "G4_Ar",
                         "CALCIUM": "G4_Ca",
                         "TIN": "G4_Sn",
                         "TUNGSTEN": "G4_W",
                         "TITANIUM": "G4_Ti",
                         "NICKEL": "G4_Ni",
                         "WATER": "G4_WATER",
                         "POLYSTYR": "G4_POLYSTYRENE",
                         "PLASCINT": None,
                         "PMMA": "G4_LUCITE", # Acrylic
                         "BONECOMP": None,
                         "BONECORT": None,
                         "MUSCLESK": None,
                         "MUSCLEST": None,
                         "ADTISSUE": None,
                         "KAPTON": "G4_KAPTON",
                         "POLYETHY": "G4_POLYETHYLENE",
                         "AIR": "G4_AIR"}
