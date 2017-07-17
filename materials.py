import fluka_material_db
import pyfluka.parser
import warnings


FLUKA_G4_MATERIAL_MAP = fluka_material_db.FLUKA_G4_MATERIAL_MAP

def map_materials_to_bdsim(materials):
    pass

def get_region_material_strings(ordered_regions, cards):
    """Given an ordered list of region names and a series of cards, map
    the region names to the material names.  Does not support
    index-based assignment.

    """
    # Map of region names to their Fluka material names.
    region_material_map = dict()
    for card in cards:
        if card.keyword != "ASSIGNMA":
            continue
        _warn_assignma(card)
        material_name = card.what1
        region_lower = card.what2
        region_upper = card.what3
        # Steps must be ints or None, not merely floats with integer value.
        step = int(card.what4) if card.what4 is not None else None

        # Get the start and stop indices.
        # Slicing is exclusive on the upper bound so we have to add 1
        start_index = ordered_regions.index(region_lower)
        if region_upper != region_lower and region_upper != None:
            stop_index = ordered_regions.index(region_upper) + 1
        else:
            stop_index = start_index + 1

        for region_name in ordered_regions[start_index:stop_index:step]:
            region_material_map[region_name] = material_name

    return region_material_map


def _warn_assignma(card):
    material_name = card.what1
    lower_bound = card.what2
    upper_bound = card.what3
    field_present = card.what5
    if field_present is not None:
        msg = "Fields present in at least one region according to ASSIGNMA cards."
        warnings.warn(msg)

    def any_indices(columns):
        return any([is_index(column) for column in columns])

    if any_indices([lower_bound, upper_bound, material_name]):
        msg = "Index-based input not supported for material assignment."
        raise RuntimeError(msg)
    return _warn_assignma


def is_index(column):
    """Check if the column is an index (i.e coercable to int)."""
    # Do not necessarily support index-based input.  Best to warn than silently
    # and mysteriously fail.
    try:
        int(column)
        return True
    except:
        return False


def generate_bdsim_materials():
    pass
