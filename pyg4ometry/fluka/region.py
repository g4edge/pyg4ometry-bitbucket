import itertools
import logging
from copy import deepcopy
from uuid import uuid4

import networkx as nx

from pyg4ometry.exceptions import FLUKAError, NullMeshError
import pyg4ometry.geant4 as g4
from pyg4ometry.transformation import matrix2tbxyz, tbxyz2matrix, reverse
from pyg4ometry.fluka.body import BodyMixin
from .vector import Three, Extent, areExtentsOverlapping

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class _Boolean(object):
    def generate_name(self, index, rootname=None):
        """Try to generate a sensible name for intermediate
        Geant4 booleans which have no FLUKA analogue."""
        if rootname is None:
            rootname = "a{}".format(uuid4()).replace("-", "")

        type_name = type(self).__name__
        type_name = type_name[:3]


        if isinstance(self.body, BodyMixin):
            return "{}{}_{}_{}".format(type_name,
                                       index,
                                       self.body.name,
                                       rootname)
        elif isinstance(self.body, Zone):
            return "{}{}_{}_{}".format(type_name,
                                       index,
                                       "zone",
                                       rootname)


class Subtraction(_Boolean):
    def __init__(self, body):
        self.body = body
        self._typestring = "sub"

class Intersection(_Boolean):
    def __init__(self, body):
        self.body = body
        self._typestrin = "int"

class Union(_Boolean):
    def __init__(self, body):
        self.body = body
        self._typestring = "uni"

class Zone(object):
    def __init__(self, name=None):
        self.intersections = []
        self.subtractions = []
        self.name = name

    def addSubtraction(self, body):
        self.subtractions.append(Subtraction(body))

    def addIntersection(self,body):
        self.intersections.append(Intersection(body))

    def centre(self, referenceExtent=None):
        body_name = self.intersections[0].body.name
        referenceExtent = _getReferenceExtent(referenceExtent,
                                              self.intersections[0])
        return self.intersections[0].body.centre(
            referenceExtent=referenceExtent)

    def rotation(self):
        return self.intersections[0].body.rotation()

    def tbxyz(self):
        return matrix2tbxyz(self.rotation())

    def _getSolidFromBoolean(self, boolean, reg, referenceExtent):
        try:
            return reg.solidDict[boolean.body.name]
        except KeyError:
            referenceExtent = _getReferenceExtent(referenceExtent, boolean)
            return boolean.body.geant4Solid(reg,
                                            referenceExtent=referenceExtent)

    def geant4Solid(self, reg, referenceExtent=None):
        try:
            body0 = self.intersections[0].body
        except IndexError:
            raise FLUKAError("zone has no +.")

        result = self._getSolidFromBoolean(self.intersections[0],
                                           reg,
                                           referenceExtent)

        booleans = self.intersections + self.subtractions

        for boolean,i in zip(booleans[1:],range(0,len(booleans[1:])+2)):
            boolean_name = boolean.generate_name(i, rootname=self.name)

            tra2 = _get_tra2(body0, boolean.body, referenceExtent)
            other_solid = self._getSolidFromBoolean(boolean, reg,
                                                    referenceExtent)
            if isinstance(boolean, Subtraction):
                result = g4.solid.Subtraction(boolean_name,
                                              result, other_solid,
                                              tra2, reg)

            elif isinstance(boolean, Intersection):
                result = g4.solid.Intersection(boolean_name,
                                               result, other_solid,
                                               tra2, reg)
        return result

    def flukaFreeString(self):
        fs = ""

        booleans = self.intersections + self.subtractions
        for s in booleans:
            if isinstance(s,Intersection) :
                if isinstance(s.body,Zone) :
                    fs = fs+" +("+s.body.flukaFreeString()+")"
                else :
                    fs=fs+" +"+s.body.name
            elif isinstance(s,Subtraction) :
                if isinstance(s.body,Zone) :
                    fs = fs+" -("+s.body.flukaFreeString()+")"
                else :
                    fs=fs+" -"+s.body.name
        return fs

    def withLengthSafety(self, bigger_flukareg, smaller_flukareg,
                           shrink_intersections):
        zone_out = Zone(name=self.name)
        logger.debug("zone.name = %s", self.name)
        for boolean in self.intersections:
            body = boolean.body
            name = body.name

            if isinstance(body, Zone):
                zone_out.addIntersection(body.withLengthSafety(
                    bigger_flukareg,
                    smaller_flukareg,
                    shrink_intersections))
            elif shrink_intersections:
                ls_body = deepcopy(smaller_flukareg.getBody(name))
                ls_body.name += "_s"
                logger.debug("Adding shrunk intersection %s to registry",
                             ls_body.name)
                zone_out.addIntersection(ls_body)
            else:
                ls_body = deepcopy(bigger_flukareg.getBody(name))
                ls_body.name += "_e"
                logger.debug("Adding expanded intersection %s to registry",
                             ls_body.name)
                zone_out.addIntersection(ls_body)

        for boolean in self.subtractions:
            body = boolean.body
            name = body.name
            if isinstance(body, Zone):
                zone_out.addSubtraction(body.withLengthSafety(
                    bigger_flukareg,
                    smaller_flukareg,
                    not shrink_intersections)) # flip length safety
                # convention if entering a subtracted subzone.
            elif shrink_intersections:
                ls_body = deepcopy(bigger_flukareg.getBody(name))
                ls_body.name += "_e"
                logger.debug("Adding expanded subtraction %s to registry",
                             ls_body.name)
                zone_out.addSubtraction(ls_body)
            else:
                ls_body = deepcopy(smaller_flukareg.getBody(name))
                ls_body.name += "_s"
                logger.debug("Adding shrunk subtraction %s to registry",
                             ls_body.name)
                zone_out.addSubtraction(ls_body)
        return zone_out

    def allBodiesToRegistry(self, flukaregistry):
        for boolean in self.intersections + self.subtractions:
            body = boolean.body
            name = body.name
            if isinstance(body, Zone):
                body.allBodiesToRegistry(flukaregistry)
            elif name not in flukaregistry.bodyDict:
                flukaregistry.addBody(body)

    def bodies(self):
        bodies = set()
        for boolean in self.intersections + self.subtractions:
            body = boolean.body
            name = body.name
            if isinstance(body, Zone):
                bodies = bodies.union(body.bodies())
            else:
                bodies.add(body)
        return bodies

    def removeBody(self, name):
        newIntersections = []
        for intsx in self.intersections:
            if isinstance(intsx, Zone):
                intsx.body.removeBody(name)
                newIntersections.append(intsx)
            elif intsx.body.name != name:
                newIntersections.append(intsx)

        newSubtractions = []
        for subt in self.subtractions:
            if isinstance(subt, Zone):
                subt.body.removeBody(name)
                newSubtractions.append(subt)
            elif subt.body.name != name:
                newSubtractions.append(subt)

        self.intersections = newIntersections
        self.subtractions = newSubtractions

    def makeUnique(self, nameSuffix, flukaregistry):
        """Get this zone with every constituent body recreated with a
        unique name by appending nameSuffix.

        :param nameSuffix: The string to append to the names of the
        bodies.
        :param flukaregistry: the FlukaRegisytr instance to add the
        uniquely defined bodies to.
        """

        result = Zone()
        nestedZoneCount = 0
        for boolean in self.intersections + self.subtractions:
            body = boolean.body
            if body.name is None: # e.g. a zone with no name
                name = "zone{}_{}".format(nestedZoneCount, nameSuffix)
                nestedZoneCount += 1
            else:
                name = body.name + nameSuffix

            booleanType = type(boolean)

            if isinstance(body, Zone):
                if booleanType is Intersection:
                    result.addIntersection(body.makeUnique(
                        flukaregistry=flukaregistry,
                        nameSuffix=nameSuffix))
                elif booleanType is Subtraction:
                    result.addSubtraction(body.makeUnique(
                        flukaregistry=flukaregistry,
                        nameSuffix=nameSuffix))
            else:
                if name in flukaregistry.bodyDict:
                    newBody = flukaregistry.getBody(name)
                else:
                    newBody = deepcopy(body)
                    newBody.name = name
                    flukaregistry.addBody(newBody)

                if booleanType is Intersection:
                    result.addIntersection(newBody)
                elif booleanType is Subtraction:
                    result.addSubtraction(newBody)
                else:
                    raise ValueError("Unknown Boolean type")
        return result


class Region(object):

    def __init__(self, name, material=None, comment = ""):
        self.name = name
        self.zones = []
        self.material = material
        self.comment = comment

    def addZone(self,zone):
        self.zones.append(zone)

    def centre(self, referenceExtent=None):
        return self.zones[0].centre(referenceExtent=referenceExtent)

    def tbxyz(self):
        return self.zones[0].tbxyz()

    def rotation(self):
        return self.zones[0].rotation()

    def bodies(self):
        bodies = set()
        for zone in self.zones:
            bodies = bodies.union(zone.bodies())
        return bodies

    def geant4Solid(self, reg, referenceExtent=None):
        logger.debug("Region = %s", self.name)
        try:
            zone0 = self.zones[0]
        except IndexError:
            raise FLUKAError("Region {} has no zones.".format(self.name))

        result = zone0.geant4Solid(reg, referenceExtent=referenceExtent)
        for zone,i in zip(self.zones[1:],range(1,len(self.zones[1:])+1)):
            try:
                otherg4 = zone.geant4Solid(reg, referenceExtent=referenceExtent)
            except FLUKAError as e:
                msg = e.message
                raise FLUKAError("In region {}, {}".format(self.name, msg))
            zone_name = "{}_union_z{}".format(self.name, i)
            tra2 = _get_tra2(zone0, zone, referenceExtent=referenceExtent)
            logger.debug("union tra2 = %s", tra2)
            result  = g4.solid.Union(zone_name, result, otherg4, tra2, reg)

        return result

    def flukaFreeString(self):
        #fs = "region "+self.name
        fs = self.name+" "+str(5)

        for z in self.zones :
            fs=fs+" | "+z.flukaFreeString()

        if self.comment != "" :
            fs = "* "+self.comment+"\n"+fs

        return fs

    def withLengthSafety(self, bigger_flukareg, smaller_flukareg):
        result = Region(self.name, material=self.material)
        for zone in self.zones:
            result.addZone(zone.withLengthSafety(bigger_flukareg,
                                                 smaller_flukareg,
                                                 shrink_intersections=True))
        return result


    def allBodiesToRegistry(self, registry):
        for zone in self.zones:
            zone.allBodiesToRegistry(registry)

    def zoneGraph(self, referenceExtent=None):
        zones = self.zones
        n_zones = len(zones)

        tried = []
        # Build undirected graph, and add nodes corresponding to each zone.
        graph = nx.Graph()
        graph.add_nodes_from(range(n_zones))
        if n_zones == 1: # return here if there's only one zone.
            return nx.connected_components(graph)

        # Get extent for each zone
        zone_extents = self._get_zone_extents(referenceExtent=referenceExtent)

        # Loop over all combinations of zone numbers within this region
        for i, j in itertools.product(range(n_zones), range(n_zones)):
            # Trivially connected to self or tried this combination.
            if i == j or {i, j} in tried:
                continue
            tried.append({i, j})

            # Check if the bounding boxes overlap.  Cheaper than intersecting.
            if not areExtentsOverlapping(zone_extents[i], zone_extents[j]):
                continue

            # Check if a path already exists.  Not sure how often this
            # arises but should at least occasionally save some time.
            if nx.has_path(graph, i, j):
                continue

            # Finally: we must do the intersection op.
            logger.debug("Region = %s, int zone %d with %d", self.name, i, j)
            if areOverlapping(zones[i], zones[j],
                              referenceExtent=referenceExtent):
                graph.add_edge(i, j)
        return graph

    def get_connected_zones(self, referenceExtent=None):
        return list(nx.connected_components(
            self.zoneGraph(referenceExtent=referenceExtent)))

    def _get_zone_extents(self, referenceExtent=None):
        material = g4.MaterialPredefined("G4_Galactic")
        extents = []
        for zone in self.zones:
            greg = g4.Registry()
            wlv = _make_wlv(greg)

            try:
                zone_solid = zone.geant4Solid(reg=greg,
                                              referenceExtent=referenceExtent)
            except FLUKAError as e:
                raise FLUKAError("Error in region {}: {}".format(self.name,
                                                                 e.message))

            zoneLV = g4.LogicalVolume(zone_solid,
                                      material,
                                      _random_name(),
                                      greg)
            lower, upper = zoneLV.mesh.getBoundingBox(zone.rotation(),
                                                      zone.centre())

            extents.append(Extent(lower, upper))
        return extents

    def extent(self, referenceExtent=None):
        greg = g4.Registry()
        world_solid = g4.solid.Box("world_solid", 1e4, 1e4, 1e4, greg, "mm")
        wlv = g4.LogicalVolume(world_solid,
                               g4.MaterialPredefined("G4_Galactic"),
                               "wl", greg)
        solid = self.geant4Solid(greg, referenceExtent=referenceExtent)
        regionLV = g4.LogicalVolume(solid,
                                    g4.MaterialPredefined("G4_Galactic"),
                                    "{}_lv".format(self.name),
                                    greg)

        lower, upper = regionLV.mesh.getBoundingBox(
            self.rotation(),
            self.centre(referenceExtent=referenceExtent))

        return Extent(lower, upper)

    def removeBody(self, name):
        for zone in self.zones:
            zone.removeBody(name)

    def makeUnique(self, nameSuffix, flukaregistry):
        """Get this Region instance with every constituent body
        with a unique name by appending nameSuffix to each Body
        instance.

        :param nameSuffix: string to append to each Body instance.
        :param flukaregistry: FlukaRegisty instance to add each
        newly-defined body to."""

        result = Region(self.name, self.material)
        for zone in self.zones:
            result.addZone(zone.makeUnique(flukaregistry=flukaregistry,
                                           nameSuffix=nameSuffix))
        return result


def _get_relative_rot_matrix(first, second):
    return first.rotation().T.dot(second.rotation())

def _get_relative_translation(first, second, referenceExtent):
    # In a boolean rotation, the first solid is centred on zero,
    # so to get the correct offset, subtract from the second the
    # first, and then rotate this offset with the rotation matrix.
    referenceExtent1 = _getReferenceExtent(referenceExtent, first)
    referenceExtent2 = _getReferenceExtent(referenceExtent, second)
    offset_vector = (second.centre(referenceExtent=referenceExtent2)
                     - first.centre(referenceExtent=referenceExtent1))
    mat = first.rotation().T
    offset_vector = mat.dot(offset_vector).view(Three)
    return offset_vector

def _get_relative_rotation(first, second):
    # The first solid is unrotated in a boolean operation, so it
    # is in effect rotated by its inverse.  We apply this same
    # rotation to the second solid to get the correct relative
    # rotation.
    return matrix2tbxyz(_get_relative_rot_matrix(first, second))

def _get_tra2(first, second, referenceExtent):
    relative_angles = _get_relative_rotation(first, second)
    relative_translation = _get_relative_translation(first, second,
                                                     referenceExtent)
    relative_transformation = [relative_angles, relative_translation]
    # convert to the tra2 format of a list of lists...

    logger.debug("%s, %s", first.name, second.name)
    logger.debug("relative_angles = %s", relative_angles)
    logger.debug("relative_translation = %s", relative_translation)

    relative_transformation = [list(relative_transformation[0]),
                               list(relative_transformation[1])]
    return relative_transformation

def _random_name():
    return "a{}".format(uuid4()).replace("-", "")

def _make_wlv(reg):
    world_material = g4.MaterialPredefined("G4_Galactic")
    world_solid = g4.solid.Box("world_box", 100, 100, 100, reg, "mm")
    return g4.LogicalVolume(world_solid, world_material, "world_lv", reg)

def areOverlapping(first, second, referenceExtent=None):
    greg = g4.Registry()

    solid1 = first.geant4Solid(greg, referenceExtent=referenceExtent)
    solid2 = second.geant4Solid(greg, referenceExtent=referenceExtent)

    tra2 = _get_tra2(first, second, referenceExtent)

    intersection = g4.solid.Intersection(_random_name(),
                           solid1,
                           solid2,
                           tra2,
                           greg)

    try:
        mesh = intersection.pycsgmesh()
    except NullMeshError:
        return False
    return True

def _getReferenceExtent(referenceExtent, boolean):
    """referenceExtent should really be a dictionary of 
    {bodyName: extentInstance}."""
    if isinstance(boolean, (Zone, Region)):
        return referenceExtent
    elif isinstance(boolean, _Boolean):
        body_name = boolean.body.name
    elif isinstance(boolean, BodyMixin):
        body_name = boolean.name
    else:
        raise ValueError("Unknown boolean type")

    if body_name is None:
        return referenceExtent

    if (isinstance(boolean, (Subtraction, Intersection))
            and isinstance(boolean.body, Zone)):
        return referenceExtent

    if referenceExtent is None:
        return None
    try:
        return referenceExtent[body_name]
    except AttributeError:
        raise
    except KeyError:
        # This can happen if we have provided a referenceExtentMap for
        # the Quadrics but have not yet generated extents for the
        # other bodies.
        logger.debug("%s not found in %s", body_name, referenceExtent)
        return None
