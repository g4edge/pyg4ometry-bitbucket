"""Some constants useful for converting Fluka materials to GDML materials.

FLUKA_G4_MATERIAL_MAP maps Fluka Material names to their corresponding
Geant4 material names.

CHARGE_MASS_NUMBER_MAP maps atomic numbers to their corresponding typical mass
numbers.

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

# This dictionary maps Z to A.
# Fluka lets you leave the mass number out, and it will use the
# "standard" one internally.  So I need to a place to look up the
# "standard" mass number for a given atomic number.
# Note: Fluka doesn't support atomic numbers above 100, so nor shall I
# here.

CHARGE_MASS_NUMBER_MAP = {1: 1,       # H        Hydrogen
                          2: 4,       # He         Helium
                          3: 7,       # Li        Lithium
                          4: 9,       # Be      Beryllium
                          5: 11,      # B           Boron
                          6: 12,      # C          Carbon
                          7: 14,      # N        Nitrogen
                          8: 16,      # O          Oxygen
                          9: 19,      # F        Fluorine
                          10: 20,     # Ne           Neon
                          11: 23,     # Na         Sodium
                          12: 24,     # Mg      Magnesium
                          13: 27,     # Al      Aluminium
                          14: 28,     # Si        Silicon
                          15: 31,     # P      Phosphorus
                          16: 32,     # S          Sulfur
                          17: 35,     # Cl       Chlorine
                          18: 40,     # Ar          Argon
                          19: 30,     # K       Potassium
                          20: 40,     # Ca        Calcium
                          21: 45,     # Sc       Scandium
                          22: 48,     # Ti       Titanium
                          23: 51,     # V        Vanadium
                          24: 52,     # Cr       Chromium
                          25: 55,     # Mn      Manganese
                          26: 56,     # Fe           Iron
                          27: 58,     # Co         Cobalt
                          28: 58,     # Ni         Nickel
                          29: 64,     # Cu         Copper
                          30: 65,     # Zn           Zinc
                          31: 70,     # Ga        Gallium
                          32: 73,     # Ge      Germanium
                          33: 75,     # As        Arsenic
                          34: 79,     # Se       Selenium
                          35: 80,     # Br        Bromine
                          36: 84,     # Kr        Krypton
                          37: 85,     # Rb       Rubidium
                          38: 88,     # Sr      Strontium
                          39: 89,     # Y         Yttrium
                          40: 91,     # Zr      Zirconium
                          41: 93,     # Nb        Niobium
                          42: 96,     # Mo     Molybdenum
                          43: 98,     # Tc     Technetium
                          44: 101,    # Ru      Ruthenium
                          45: 103,    # Rh        Rhodium
                          46: 106,    # Pd      Palladium
                          47: 108,    # Ag         Silver
                          48: 112,    # Cd        Cadmium
                          49: 115,    # In         Indium
                          50: 119,    # Sn            Tin
                          51: 122,    # Sb       Antimony
                          52: 128,    # Te      Tellurium
                          53: 127,    # I          Iodine
                          54: 131,    # Xe          Xenon
                          55: 133,    # Cs         Cesium
                          56: 137,    # Ba         Barium
                          57: 139,    # La      Lanthanum
                          58: 140,    # Ce         Cerium
                          59: 141,    # Pr   Praseodymium
                          60: 144,    # Nd      Neodymium
                          61: 145,    # Pm     Promethium
                          62: 150,    # Sm       Samarium
                          63: 152,    # Eu       Europium
                          64: 157,    # Gd     Gadolinium
                          65: 159,    # Tb        Terbium
                          66: 163,    # Dy     Dysprosium
                          67: 165,    # Ho        Holmium
                          68: 167,    # Er         Erbium
                          69: 169,    # Tm        Thulium
                          70: 173,    # Yb      Ytterbium
                          71: 175,    # Lu       Lutetium
                          72: 178,    # Hf        Hafnium
                          73: 181,    # Ta       Tantalum
                          74: 184,    # W        Tungsten
                          75: 186,    # Re        Rhenium
                          76: 190,    # Os         Osmium
                          77: 192,    # Ir        Iridium
                          78: 195,    # Pt       Platinum
                          79: 197,    # Au           Gold
                          80: 201,    # Hg        Mercury
                          81: 204,    # Tl       Thallium
                          82: 207,    # Pb           Lead
                          83: 209,    # Bi        Bismuth
                          84: 209,    # Po       Polonium
                          85: 210,    # At       Astatine
                          86: 222,    # Rn          Radon
                          87: 223,    # Fr       Francium
                          88: 226,    # Ra         Radium
                          89: 227,    # Ac       Actinium
                          90: 232,    # Th        Thorium
                          91: 231,    # Pa   Protactinium
                          92: 238,    # U         Uranium
                          93: 237,    # Np      Neptunium
                          94: 244,    # Pu      Plutonium
                          95: 243,    # Am      Americium
                          96: 247,    # Cm         Curium
                          97: 247,    # Bk      Berkelium
                          98: 251,    # Cf    Californium
                          99: 252,    # Es    Einsteinium
                          100: 257}   # Fm        Fermium
