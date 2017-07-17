import fluka_material_db
import pygdml.material as pygdmlmat
import pyfluka.parser
import warnings

# For conversion we currently handle 3 cards, MATERIAL, COMPOUND, and MAT-PROP.

# These are the keywords this module will so something with.  Everything else
# will be skipped / ignored.
FLUKA_G4_MATERIAL_MAP = fluka_material_db.FLUKA_G4_MATERIAL_MAP
CHARGE_MASS_NUMBER_MAP = fluka_material_db.CHARGE_MASS_NUMBER_MAP

_COLUMNS = set(pyfluka.parser.Card._fields)

# List of keywords of cards which are supported, along with their columns which
# are also supported.
SUPPORTED_CARDS = {"MATERIAL": _COLUMNS - {"what4", "what5", "what6"},
                   "COMPOUND": [],
                   "MAT-PROP": [],
                   "ASSIGNMA": []}

# Basic idea: If there is a WHAT1 specified, then it is definitely SHOULD NOT be
# coupled to a COMPOUND card.  Defensively check this..  maybe it is still
# possible to later override knowing Fluka!

def get_region_material_strings(ordered_regions):
    pass

def map_materials_to_bdsim(materials):
    pass

def convert_cards(cards):
    """Convert a list of cards to pygdml materials.  cards should be an iterable
    of Card instances."""
    materials = dict()
    for card in cards:
        if card.keyword not in SUPPORTED_CARDS:
            continue
        elif card.keyword == "MATERIAL":
            card.warn_not_supported(SUPPORTED_CARDS["MATERIAL"])

def process_material_card(card):
    if card.what1 is not None:
        return process_element(card)

def process_element(card):
    atomic_number  = card.what1
    if card.what2 is not None:
        atomic_weight = card.what2
    else:
        atomic_weight = CHARGE_MASS_NUMBER_MAP[atomic_number]
    if card.what6 is not None and card.what6 != 0:
        mass_number = atomic_weight
    else:
        mass_number = card.what6
    density = card.what3
    name = card.sdum

    gas_cutoff = 0.01
    if density < gas_cutoff:
        state = "gas"
        pressure = pygdmat.STANDARD_PRESSURE
    else:
        state = "solid" # the default state

    # Put the info pertaining to the atomic properties into a gmdl isotope
    gdml_isotope = pygdmlmat.Isotope("{}_isotope".format(name),
                                     atomic_number,
                                     mass_number,
                                     atomic_weight)

    return pygdmlmat.Material(name, density, gdml_isotope, state=state)
