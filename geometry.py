""" A collection of classes for representing Fluka regions, zones, and bodies.

Note:  All units are in millimetres, c.f. centimetres in Fluka.

"""

from collections import namedtuple
import math as _math
import numpy as _np
from numpy import pi as _pi
from uuid import uuid4 as _uuid4
from operator import add, sub, or_

import pygdml as _pygdml
from pygdml import transformation as _trf
import vector

# Tolerance when minimising solids.  In this case:  5% longer than the
# resulting mesh.
MINTOL = 1.05

class Body(object):
    """A class representing a body as defined in Fluka.
    get_body_as_gdml_solid() returns the body as a pygdml.solid

    """

    def __init__(self,
                 name,
                 translation,
                 transformation):

        self.name = name
        self._translation = translation
        self._transformation = transformation
        # Named tuple constructor for later use.

    def view(self, setclip=True):
        w = _pygdml.solid.Box("world", 10000, 10000, 10000)
        world_volume = _pygdml.Volume([0, 0, 0], [0, 0, 0], w,
                                      "world-volume", None,
                                      1, False, "G4_NITROUS_OXIDE")

        self.add_to_volume(world_volume)
        if setclip is True:
            world_volume.setClip()
        mesh = world_volume.pycsgmesh()
        viewer = _pygdml.VtkViewer()
        viewer.addSource(mesh)
        viewer.view()

    def _apply_crude_scale(self, scale):
        self._scale = scale

    def _apply_extent(self, extent):
        pass

    def add_to_volume(self, volume):
        """Basically for adding to a world volume.

        """
        solid = self.gdml_solid()
        # Convert the matrix to TB xyz:
        rotation_angles = _trf.matrix2tbxyz(self.rotation)
        # Up to this point all rotations are active, which is OK
        # because so are boolean rotations.  However, volume rotations
        # are passive, so reverse the rotation:
        rotation_angles = _trf.reverse(rotation_angles)
        _pygdml.volume.Volume(rotation_angles,
                              self.centre(),
                              self.gdml_solid(),
                              self.name,
                              volume,
                              1,
                              False,
                              "G4_Galactic")


    def resize(self, scale):
        """Return this instance bounded or extented according to the
        parameter "scale".

        """
        if isinstance(scale, (float, int)):
            self._apply_crude_scale(scale)
        elif isinstance(scale, Body):
            extent = self._get_overlap(scale)
            self._apply_extent(extent)
        else:
            raise TypeError("Unknown scale type: {}".format(type(scale)))
        return self

    def __call__(self, scale):
        return self.resize(scale)

    def _extent(self):
        # Construct a world volume to place the solid in to be meshed.
        w = _pygdml.solid.Box("world", 10000, 10000, 10000)
        world_volume = _pygdml.Volume([0, 0, 0], [0, 0, 0], w,
                                      "world-volume", None,
                                      1, False, "G4_NITROUS_OXIDE")
        self.add_to_volume(world_volume)
        return Extent.from_wv(world_volume)

    def _get_overlap(self, other):
        """
        Get the overlap of this solid with another, calculate the
        extent of the mesh, and return this.

        """
        intersection = self + other
        extent = intersection._extent()
        return extent

    def intersect(self, other=None):
        """
        Intersect this solid with another solid.

        """
        if other is None:
            return self
        return self + other

    def subtract(self, other=None):
        """
        Subtract from this solid another solid.

        """
        if other is None:
            return self
        return self - other

    def union(self, other=None):
        """
        Boolean union of this solid with another solid.

        """
        if other is None:
            return self
        return self | other

    def __add__(self, other):
        """Perform the intersection of this solid with another.

        """
        output_name = self._generate_name(other)

        relative_translation = self._get_relative_translation(other)
        relative_angles = self._get_relative_rotation(other)
        relative_transformation = [relative_angles, relative_translation]

        output_solid = _pygdml.solid.Intersection(output_name,
                                                  self.gdml_solid(),
                                                  other.gdml_solid(),
                                                  relative_transformation)
        output_centre = self.centre()
        output_rotation = self.rotation

        return Boolean(output_name,
                       output_solid,
                       output_centre,
                       output_rotation)

    def __sub__(self, other):
        output_name = self._generate_name(other)

        relative_translation = self._get_relative_translation(other)
        relative_angles = self._get_relative_rotation(other)
        relative_transformation = [relative_angles, relative_translation]

        output_solid = _pygdml.solid.Subtraction(output_name,
                                                 self.gdml_solid(),
                                                 other.gdml_solid(),
                                                 relative_transformation)
        output_centre = self.centre()
        output_rotation = self.rotation
        return Boolean(output_name,
                       output_solid,
                       output_centre,
                       output_rotation)

    def __or__(self, other):
        output_name = self._generate_name(other)

        relative_translation = self._get_relative_translation(other)
        relative_angles = self._get_relative_rotation(other)
        relative_transformation = [relative_angles, relative_translation]

        output_centre = self.centre()
        output_rotation = self.rotation

        output_solid = _pygdml.Union(output_name,
                                     self.gdml_solid(),
                                     other.gdml_solid(),
                                     relative_transformation)

        return Boolean(output_name,
                       output_solid,
                       output_centre,
                       output_rotation)

    def _get_relative_rot_matrix(self, other):
        return self.rotation.T.dot(other.rotation)

    def _get_relative_translation(self, other):
        # In a boolean rotation, the first solid is centred on zero,
        # so to get the correct offset, subtract from the second the
        # first, and then rotate this offset with the rotation matrix.
        offset_vector =  vector.Three((other.centre().x - self.centre().x),
                                      (other.centre().y - self.centre().y),
                                      (other.centre().z - self.centre().z))
        mat = self.rotation.T
        offset_vector = mat.dot(offset_vector).view(vector.Three)
        try:
            x = offset_vector[0][0]
            y = offset_vector[0][1]
            z = offset_vector[0][2]
        except IndexError:
            x = offset_vector.x
            y = offset_vector.y
            z = offset_vector.z
        return vector.Three(x,y,z)

    def _get_relative_rotation(self, other):
        # The first solid is unrotated in a boolean operation, so it
        # is in effect rotated by its inverse.  We apply this same
        # rotation to the second solid to get the correct relative
        # rotation.
        return _trf.matrix2tbxyz(self._get_relative_rot_matrix(other))

    def _generate_name(self, other):
        """
        Generate an output  name given the two solids.  Keeps sane
        names for sufficiently short output, but returns a
        universally unique identifier for longer names.  This is
        required as names will rapidly becoming massive for complex
        geometries, resulting in a massive output file.

        """
        if len(self.name) + len(other.name) < 36:
            return self.name + "_" +  other.name
        else:
            # GDML name has to start with a letter so append an "a".
            return "a" + str(_uuid4())


class RPP(Body):
    """
    An RPP is a rectangular parallelpiped (a cuboid).
    """
    def __init__(self, name, parameters,
                 translation=None,
                 transformation=None):
        super(RPP, self).__init__(name,
                                  translation,
                                  transformation)

        self._set_parameters(parameters)
        self._set_rotation_matrix(transformation)

        if (self.parameters.x_min > self.parameters.x_max or
            self.parameters.y_min > self.parameters.y_max or
            self.parameters.z_min > self.parameters.z_max):
            raise Warning("This RPP \"" + name + "\" has mins larger than "
                          "its maxes.\n It is ignored in Fluka but "
                          "won't be ignored here!")


    def _set_parameters(self, parameters):
        parameter_names =  ['x_min', 'x_max', 'y_min',
                            'y_max', 'z_min', 'z_max']
        self.parameters = Parameters(zip(parameter_names, parameters))
        # Hidden versions of these parameters which can be reassigned
        self._x_min = self.parameters.x_min
        self._x_max = self.parameters.x_max
        self._y_min = self.parameters.y_min
        self._y_max = self.parameters.y_max
        self._z_min = self.parameters.z_min
        self._z_max = self.parameters.z_max

    def _apply_extent(self, extent):
        if self._x_min < MINTOL * extent.lower.x:
            self._x_min = MINTOL * extent.lower.x
        if self._x_max > MINTOL * extent.upper.x:
            self._x_max = MINTOL * extent.upper.x
        if self._y_min < MINTOL * extent.lower.y:
            self._y_min = MINTOL * extent.lower.y
        if self._y_max > MINTOL * extent.upper.y:
            self._y_max = MINTOL * extent.upper.y
        if self._z_min < MINTOL * extent.lower.z:
            self._z_min = MINTOL * extent.lower.z
        if self._z_max > MINTOL * extent.upper.z:
            self._z_max = MINTOL * extent.upper.z

    def centre(self):
        """
        Return the coordinates of the centre of the Rectangular
        Parallelepiped (cuboid).

        """

        return 0.5 * vector.Three(self._x_min + self._x_max,
                                  self._y_min + self._y_max,
                                  self._z_min + self._z_max)

    def _set_rotation_matrix(self, transformation):
        self.rotation = _np.matrix(_np.identity(3))

    def crude_extent(self):
        return max([abs(self.parameters.x_min), abs(self.parameters.x_max),
                    abs(self.parameters.y_min), abs(self.parameters.y_max),
                    abs(self.parameters.z_min), abs(self.parameters.z_max),
                    self.parameters.x_max - self.parameters.x_min,
                    self.parameters.y_max - self.parameters.y_min,
                    self.parameters.z_max - self.parameters.z_min])


    def gdml_solid(self):
        """
        Construct a pygdml Box from this body definition
        """
        x_length = self._x_max - self._x_min
        y_length = self._y_max - self._y_min
        z_length = self._z_max - self._z_min

        return _pygdml.solid.Box(self.name,
                                 0.5 * x_length,
                                 0.5 * y_length,
                                 0.5 * z_length)


class SPH(Body):
    def __init__(self, name, parameters,
                 translation=None,
                 transformation=None):

        super(SPH, self).__init__(name,
                                  translation,
                                  transformation)
        self._set_parameters(parameters)
        self._set_rotation_matrix(transformation)

    def _set_parameters(self, parameters):
        parameter_names =  ['v_x', 'v_y', 'v_z', 'radius']
        self.parameters = Parameters(zip(parameter_names, parameters))

    def centre(self):
        """
        Returns the coordinates of the centre of the sphere in
        MILLIMETRES, as this is used for GDML.

        """
        return vector.Three(self.parameters.v_x,
                            self.parameters.v_y,
                            self.parameters.v_z)

    def _set_rotation_matrix(self, transformation):
        self.rotation = _np.matrix(_np.identity(3))

    def crude_extent(self):
        return max(map(abs, self.parameters))

    def gdml_solid(self):
        """
        Construct a solid, whole, GDML sphere from this.

        """
        return _pygdml.solid.Orb(self.name, self.parameters.radius)


class RCC(Body):
    """
    Right-angled Circular Cylinder

    Parameters:
    v_(x,y,z) = coordinates of the centre of one of the circular planes
    faces
    h_(x,y,z) = components of vector pointing in the direction of the
    other plane face, with magnitude equal to the cylinder length.
    radius    = cylinder radius
    """

    def __init__(self, name,
                 parameters,
                 translation=None,
                 transformation=None):
        super(RCC, self).__init__(name,
                                  translation,
                                  transformation)
        self._set_parameters(parameters)
        self._set_rotation_matrix(transformation)
        self._offset = vector.Three(0, 0, 0)

    def _set_parameters(self, parameters):
        parameter_names = ['v_x', 'v_y', 'v_z', 'h_x', 'h_y', 'h_z', 'radius']
        self.parameters = Parameters(zip(parameter_names, parameters))

        self.face_centre = vector.Three(self.parameters.v_x,
                                        self.parameters.v_y,
                                        self.parameters.v_z)
        self.direction = vector.Three(self.parameters.h_x,
                                      self.parameters.h_y,
                                      self.parameters.h_z)
        self.length = _np.linalg.norm(self.direction)
        self._scale = self.length

    def _apply_crude_scale(self, scale):
        self._offset = vector.Three(0, 0, 0)
        self._scale = self.length

    def _apply_extent(self, extent):
        return
        # Max possible length of a solid for the given extents:
        max_length = _np.linalg.norm([extent.size.x,
                                      extent.size.y,
                                      extent.size.z])
        # If the length is possibly smaller than the length of the
        # resulting solid, then just return the length and position unchanged.
        if self.length < max_length:
            self._offset = vector.Three(0, 0, 0)
            self._scale = self.length
        # Else shorten and reposition the cylinder.
        else:
            # If the RCC is much longer than the maximum possible extent, I want
            # to minimise the length and centre the RCC on the point
            # closest to the centre of the mesh (while maintaining the
            # orientation of the cylinder).  The two subtractions
            # are to cancel with the terms in the RCC.centre method,
            # leaving just the point on the line closest to the cetnre.
            self._offset = (vector.point_on_line_closest_to_point(
                extent.centre,
                self.face_centre,
                self.direction)
                            - self.face_centre
                            - 0.5 * self.direction)
            self._scale = max_length * MINTOL

    def centre(self):
        """
        Returns the coordinates of the centre of the sphere in
        MILLIMETRES, as this is used for GDML.
        """

        return (self._offset
                + self.face_centre
                + (0.5 * self.direction))

    def _set_rotation_matrix(self, transformation):
        initial = [0, 0, 1]
        final = -self.direction
        self.rotation = _trf.matrix_from(initial, final)

    def crude_extent(self):
        centre_max = max(abs(vector.Three(self.parameters.v_x,
                                          self.parameters.v_y,
                                          self.parameters.v_z)))
        return centre_max + self.length

    def gdml_solid(self):
        return _pygdml.solid.Tubs(self.name, 0.0,
                                  self.parameters.radius,
                                  self._scale * 0.5,
                                  0.0,
                                  2*_pi)


class REC(Body):
    """
    NOT IMPLEMENTED

    Class representing the Right Elliptical Cylinder of Fluka.

    Parameters:
    face_centre_x : x-coordinate of the centre of one of the faces.
    face_centre_y : y-coordinate of the centre of one of the faces.
    face_centre_z : z-coordinate of the centre of one of the faces.

    to_other_face_x : x-component of the vector pointing from
                      face_centre to the other face.
    to_other_face_y : y-component of the vector pointing from
                      face_centre to the other face.
    to_other_face_z : z-component of the vector pointing from
                      face_centre to the other face.
    The length of the vector to_other_face is the length of the
    elliptical cylinder.

    semi_minor_x : x-component of the semi-minor axis.
    semi_minor_y : y-component of the semi-minor axis.
    semi_minor_z : z-component of the semi-minor axis.
    The length of the vector semi_minor is the length of the
    semi-minor axis.

    semi_major_x : x-component of the semi-major axis.
    semi_major_y : y-component of the semi-major axis.
    semi_major_z : z-component of the semi-major axis.
    The length of the vector semi_major is the length of the
    semi-major axis.
    """
    def __init__(self, name,
                 parameters,
                 translation=None,
                 transformation=None):
        super(REC, self).__init__(name,
                                  translation,
                                  transformation)

        self._set_parameters(parameters)
        self._set_rotation_matrix(transformation)
        raise NotImplementedError

    def _set_parameters(self, parameters):
        parameter_names = [
            "face_centre_x", "face_centre_y", "face_centre_z",
            "to_other_face_x", "to_other_face_y", "to_other_face_z",
            "semi_minor_x", "semi_minor_y", "semi_minor_z",
            "semi_major_x", "semi_major_y", "semi_major_z"]
        self.parameters = Parameters(zip(parameter_names, parameters))

    def centre(self):
        centre_x = (self.parameters.face_centre_x
                    + self.parameters.to_other_face_x * 0.5)
        centre_y = (self.parameters.face_centre_y
                    + self.parameters.to_other_face_y * 0.5)
        centre_z = (self.parameters.face_centre_z
                    + self.parameters.to_other_face_z * 0.5)

        return vector.Three(centre_x, centre_y, centre_z)

    def _set_rotation_matrix(self, transformation):
        pass

    def gdml_solid(self):
        # EllipticalTube is defined in terms of half-lengths in x, y,
        # and z.  Choose semi_major to start in the positive y direction.
        semi_minor = _np.linalg.norm([self.parameters.semi_minor_x,
                                      self.parameters.semi_minor_y,
                                      self.parameters.semi_minor_z])

        semi_major = _np.linalg.norm([self.parameters.semi_major_x,
                                      self.parameters.semi_major_y,
                                      self.parameters.semi_major_z])

        length = _np.linalg.norm([self.parameters.to_other_face_x,
                                  self.parameters.to_other_face_y,
                                  self.parameters.to_other_face_z])

        return _pygdml.solid.EllipticalTube(self.name,
                                            semi_minor,
                                            semi_major,
                                            length * 0.5)


class TRC(Body):
    """
    Truncated Right-angled Cone.

    Parameters
    ----------

    centre_major_x : x-coordinate of the centre of the larger face.
    centre_major_y : y-coordinate of the centre of the larger face.
    centre_major_z : z-coordinate of the centre of the larger face.

    major_to_minor_x : x_coordinator of the vector pointing from the major
                       to minor face.
    major_to_minor_y : y_coordinator of the vector pointing from the major
                       to minor face.
    major_to_minor_z : z_coordinator of the vector pointing from the major
                       to minor face.
    The length of the major_to_minor vector is the length of the resulting
    cone.

    major_radius : radius of the larger face.
    minor_radius : radius of the smaller face.
    """

    def __init__(self, name,
                 parameters,
                 translation=None,
                 transformation=None):
        super(TRC, self).__init__(name,
                                  translation,
                                  transformation)
        self._set_parameters(parameters)
        self.major_centre = vector.Three([self.parameters.centre_major_x,
                                          self.parameters.centre_major_y,
                                          self.parameters.centre_major_z])
        self.major_to_minor = vector.Three([self.parameters.major_to_minor_x,
                                            self.parameters.major_to_minor_y,
                                            self.parameters.major_to_minor_z])
        self.length = self.major_to_minor.length
        self._set_rotation_matrix(transformation)

    def _set_parameters(self, parameters):
        parameter_names = ['centre_major_x',
                           'centre_major_y',
                           'centre_major_z',
                           'major_to_minor_x',
                           'major_to_minor_y',
                           'major_to_minor_z',
                           'major_radius',
                           'minor_radius']
        self.parameters = Parameters(zip(parameter_names, parameters))

    def centre(self):
        return self.major_centre + 0.5 * self.major_to_minor

    def _set_rotation_matrix(self, transformation):
        # We choose in the as_gdml_solid method to place the major at
        # -z, and the major at +z, hence this choice of initial and
        # final vectors:
        initial = [0, 0, 1]
        final = self.major_to_minor
        self.rotation = _trf.matrix_from(initial, final)

    def crude_extent(self):
        length = _np.linalg.norm([self.parameters.major_to_minor_x,
                                  self.parameters.major_to_minor_y,
                                  self.parameters.major_to_minor_z])

        return max(abs(self.parameters.centre_major_x) + length,
                   abs(self.parameters.centre_major_y) + length,
                   abs(self.parameters.centre_major_z) + length,
                   self.parameters.minor_radius,
                   self.parameters.major_radius)

    def gdml_solid(self):
        # The first face of pygdml.Cons is located at -z, and the
        # second at +z.  Here choose to put the major face at -z.
        return _pygdml.solid.Cons(self.name,
                                  0.0,
                                  self.parameters.major_radius,
                                  0.0,
                                  self.parameters.minor_radius,
                                  0.5 * self.length,
                                  0.0,
                                  2*_pi)


class XYP(Body):
    """
    Infinite plane perpendicular to the z-axis.
    """
    def __init__(self, name,
                 parameters,
                 translation=None,
                 transformation=None):
        super(XYP, self).__init__(name,
                                  translation,
                                  transformation)
        self._set_parameters(parameters)
        self._set_rotation_matrix(transformation)
        self._offset = vector.Three(0, 0, 0)

    def _set_parameters(self, parameters):
        parameter_names = ['v_z']
        self.parameters = Parameters(zip(parameter_names, parameters))

    def _apply_crude_scale(self, scale):
        self._offset = vector.Three(0, 0, 0)
        self._scale_x = scale
        self._scale_y = scale
        self._scale_z = scale

    def _apply_extent(self, extent):
        self._offset = vector.Three(extent.centre.x,
                                    extent.centre.y,
                                    0.0)
        self._scale_x = extent.size.x * MINTOL
        self._scale_y = extent.size.y * MINTOL
        self._scale_z = extent.size.z * MINTOL

    def centre(self):
        # Choose the face at
        centre_x = 0.0
        centre_y = 0.0
        centre_z = self.parameters.v_z - (self._scale_z * 0.5)
        return (self._offset
                + vector.Three(centre_x, centre_y, centre_z))

    def _set_rotation_matrix(self, transformation):
        self.rotation = _np.matrix(_np.identity(3))

    def crude_extent(self):
        return abs(self.parameters.v_z)

    def gdml_solid(self):
        # We choose the box face pointing in the +z direction to form
        # the plane face.
        return _pygdml.solid.Box(self.name,
                                 0.5 * self._scale_x,
                                 0.5 * self._scale_y,
                                 0.5 * self._scale_z)


class XZP(Body):
    """
    Infinite plane perpendicular to the y-axis.
    """
    def __init__(self, name,
                 parameters,
                 translation=None,
                 transformation=None):
        super(XZP, self).__init__(name,
                                  translation,
                                  transformation)
        self._set_parameters(parameters)
        self._set_rotation_matrix(transformation)

    def _set_parameters(self, parameters):
        parameter_names = ['v_y']
        self.parameters = Parameters(zip(parameter_names, parameters))

    def _apply_crude_scale(self, scale):
        self._offset = vector.Three(0, 0, 0)
        self._scale_x = scale
        self._scale_y = scale
        self._scale_z = scale

    def _apply_extent(self, extent):
        self._offset = vector.Three(extent.centre.x,
                                    0.0,
                                    extent.centre.z)
        self._scale_x = extent.size.x * MINTOL
        self._scale_y = extent.size.y * MINTOL
        self._scale_z = extent.size.z * MINTOL

    def centre(self):
        centre_x = 0.0
        centre_y = self.parameters.v_y - (self._scale_y * 0.5)
        centre_z = 0.0
        return (self._offset
                + vector.Three(centre_x, centre_y, centre_z))

    def _set_rotation_matrix(self, transformation):
        self.rotation = _np.matrix(_np.identity(3))

    def crude_extent(self):
        return abs(self.parameters.v_y)

    def gdml_solid(self):
        # We choose the box face pointing in the +y direction to form
        # the plane face.
        return _pygdml.solid.Box(self.name,
                                 0.5 * self._scale_x,
                                 0.5 * self._scale_y,
                                 0.5 * self._scale_z)


class YZP(Body):
    """ Infinite plane perpendicular to the x-axis. """
    def __init__(self, name,
                 parameters,
                 translation=None,
                 transformation=None):
        super(YZP, self).__init__(name,
                                  translation,
                                  transformation)
        self._set_parameters(parameters)
        self._set_rotation_matrix(transformation)

    def _set_parameters(self, parameters):
        parameter_names = ['v_x']
        self.parameters = Parameters(zip(parameter_names, parameters))

    def _apply_crude_scale(self, scale):
        self._offset = vector.Three(0, 0, 0)
        self._scale_x = scale
        self._scale_y = scale
        self._scale_z = scale

    def _apply_extent(self, extent):
        self._offset = vector.Three(0.0,
                                    extent.centre.y,
                                    extent.centre.z)
        self._scale_x = extent.size.x * MINTOL
        self._scale_y = extent.size.y * MINTOL
        self._scale_z = extent.size.z * MINTOL

    def centre(self):
        centre_x = self.parameters.v_x - (self._scale_x * 0.5)
        centre_y = 0.0
        centre_z = 0.0
        return (self._offset
                + vector.Three(centre_x, centre_y, centre_z))

    def _set_rotation_matrix(self, transformation):
        self.rotation = _np.matrix(_np.identity(3))

    def crude_extent(self):
        return abs(self.parameters.v_x)

    def gdml_solid(self):
        # We choose the box face pointing in the +x direction to form
        # the plane face.
        return _pygdml.solid.Box(self.name,
                                 0.5 * self._scale_x,
                                 0.5 * self._scale_y,
                                 0.5 * self._scale_z)


class PLA(Body):
    """
    Generic infinite half-space.

    Parameters:
    x_direction (Hx) :: x-component of a vector of arbitrary length
                        perpendicular to the plane.  Pointing outside
                        of the space.
    y_direction (Hy) :: y-component of a vector of arbitrary length
                        perpendicular to the plane.  Pointing outside
                        of the space.
    z_direction (Hz) :: z-component of a vector of arbitrary length
                        perpendicular to the plane.  Pointing outside
                        of the space.
    x_position  (Vx) :: x-component of a point anywhere on the plane.
    y_position  (Vy) :: y-component of a point anywhere on the plane.
    z_position  (Vz) :: z-component of a point anywhere on the plane.
    """
    def __init__(self, name,
                 parameters,
                 translation=None,
                 transformation=None):
        super(PLA, self).__init__(name,
                                  translation,
                                  transformation)
        self._set_parameters(parameters)
        self._set_rotation_matrix(transformation)

    def _set_parameters(self, parameters):
        parameter_names = ["x_direction", "y_direction", "z_direction",
                           "x_position", "y_position", "z_position"]
        self.parameters = Parameters(zip(parameter_names, parameters))


        # Normalise the perpendicular vector:
        perpendicular = vector.Three([self.parameters.x_direction,
                                      self.parameters.y_direction,
                                      self.parameters.z_direction])
        self.perpendicular = (perpendicular
                              / _np.linalg.norm(perpendicular))
        self.surface_point = vector.Three([self.parameters.x_position,
                                           self.parameters.y_position,
                                           self.parameters.z_position])
        self.surface_point = self._closest_point([0,0,0])

    def centre(self):
        # This is the centre of the underlying gdml solid (i.e. won't
        # be on the surface, but set backwards by half length scale's amount.
        centre = (self.surface_point
                  - (0.5 * self._scale * self.perpendicular.unit))
        return centre

    def _set_rotation_matrix(self, transformation):
        # Choose the face pointing in the direction of the positive
        # z-axis to make the face of the plane.
        initial = [0,0,1]
        final = self.perpendicular
        self.rotation =  _trf.matrix_from(initial, final)

    def crude_extent(self):
        return max(abs(self.surface_point.x),
                   abs(self.surface_point.y),
                   abs(self.surface_point.z))

    def _closest_point(self, point):
        """
        Return the point on the plane closest to the point provided.

        """
        # perpendicular distance from the point to the plane
        distance = _np.dot((self.surface_point - point),
                           self.perpendicular)
        closest_point = point + distance * self.perpendicular
        assert (abs(_np.dot(self.perpendicular,
                        closest_point - self.surface_point)) < 1e-6), (
                            "Point isn't on the plane!")
        return closest_point

    def gdml_solid(self):
        return _pygdml.solid.Box(self.name,
                                 0.5 * self._scale,
                                 0.5 * self._scale,
                                 0.5 * self._scale)


class XCC(Body):
    """
    Infinite circular cylinder parallel to x-axis

    parameters:

    centre_y    -- y-coordinate of the centre of the cylinder
    centre_z    -- z-coordinate of the centre of the cylinder
    radius -- radius of the cylinder
    """
    def __init__(self, name,
                 parameters,
                 translation=None,
                 transformation=None):
        super(XCC, self).__init__(name,
                                  translation,
                                  transformation)
        self._set_parameters(parameters)
        self._set_rotation_matrix(transformation)

    def _apply_crude_scale(self, scale):
        self._offset = vector.Three(0, 0, 0)
        self._scale = scale

    def _apply_extent(self, extent):
        self._offset = vector.Three(extent.centre.x,
                                    0.0,
                                    0.0)
        self._scale = extent.size.x * MINTOL

    def _set_parameters(self, parameters):
        parameter_names = ["centre_y", "centre_z", "radius"]
        self.parameters = Parameters(zip(parameter_names, parameters))

    def centre(self):
        return (self._offset
                + vector.Three(0.0,
                               self.parameters.centre_y,
                               self.parameters.centre_z))

    def _set_rotation_matrix(self, transformation):
        # Rotate pi/2 about the y-axis.
        self.rotation = _np.matrix([[ 0,  0, -1],
                                    [ 0,  1,  0],
                                    [ 1,  0,  0]])

    def crude_extent(self):
        return max(map(abs, self.parameters))

    def gdml_solid(self):
        return _pygdml.solid.Tubs(self.name, 0.0,
                                  self.parameters.radius,
                                  self._scale * 0.5,
                                  0.0,
                                  2*_pi)


class YCC(Body):
    """
    Infinite circular cylinder parallel to y-axis

    parameters:

    centre_x    -- x-coordinate of the centre of the cylinder
    centre_z    -- z-coordinate of the centre of the cylinder
    radius -- radius of the cylinder
    """
    def __init__(self, name,
                 parameters,
                 translation=None,
                 transformation=None):
        super(YCC, self).__init__(name,
                                  translation,
                                  transformation)
        self._set_parameters(parameters)
        self._set_rotation_matrix(transformation)

    def _apply_crude_scale(self, scale):
        self._offset = vector.Three(0, 0, 0)
        self._scale = scale

    def _apply_extent(self, extent):
        self._offset = vector.Three(0.0,
                                    extent.centre.y,
                                    0.0)
        self._scale = extent.size.y * MINTOL

    def _set_parameters(self, parameters):
        parameter_names = ["centre_z", "centre_x", "radius"]
        self.parameters = Parameters(zip(parameter_names, parameters))

    def centre(self):
        return (self._offset
                + vector.Three(self.parameters.centre_x,
                               0.0,
                               self.parameters.centre_z))

    def _set_rotation_matrix(self, transformation):
        # Rotate by pi/2 about the x-axis.
        self.rotation = _np.matrix([[ 1,  0,  0],
                                    [ 0,  0,  1],
                                    [ 0, -1,  0]])

    def crude_extent(self):
        return max(map(abs, self.parameters))

    def gdml_solid(self):
        return _pygdml.solid.Tubs(self.name,
                                  0.0,
                                  self.parameters.radius,
                                  self._scale * 0.5,
                                  0.0,
                                  2*_pi)


class ZCC(Body):
    """
    Infinite circular cylinder parallel to z-axis

    parameters:

    centre_x    -- x-coordinate of the centre of the cylinder
    centre_y    -- y-coordinate of the centre of the cylinder
    radius -- radius of the cylinder
    """
    def __init__(self, name,
                 parameters,
                 translation=None,
                 transformation=None):
        super(ZCC, self).__init__(name,
                                  translation,
                                  transformation)
        self._set_parameters(parameters)
        self._set_rotation_matrix(transformation)

    def _set_parameters(self, parameters):
        parameter_names = ["centre_x", "centre_y", "radius"]
        self.parameters = Parameters(zip(parameter_names, parameters))

    def _apply_crude_scale(self, scale):
        self._offset = vector.Three(0, 0, 0)
        self._scale = scale

    def _apply_extent(self, extent):
        self._offset = vector.Three(0.0,
                                    0.0,
                                    extent.centre.z)
        self._scale = extent.size.z * MINTOL

    def centre(self):
        return (self._offset
                + vector.Three(self.parameters.centre_x,
                               self.parameters.centre_y,
                               0.0))

    def _set_rotation_matrix(self, transformation):
        self.rotation = _np.matrix(_np.identity(3))

    def crude_extent(self):
        return max(map(abs, self.parameters))

    def gdml_solid(self):
        return _pygdml.solid.Tubs(self.name,
                                  0.0,
                                  self.parameters.radius,
                                  self._scale * 0.5,
                                  0.0,
                                  2*_pi)


class XEC(Body):
    """
    An infinite elliptical cylinder parallel to the x-axis.

    Parameters:

    centre_y (Ay) - y-coordinate of the centre of the ellipse face.
    centre_z (Az) - z-coordinate of the centre of the ellipse face.
    semi_axis_y (Ly) - semi-axis in the y-direction of the ellipse
    face.
    semi_axis_z (Lz) - semi-axis in the z-direction of the ellipse face.
    """

    def __init__(self, name,
                 parameters,
                 translation=None,
                 transformation=None):
        super(XEC, self).__init__(name,
                                  translation,
                                  transformation)
        self._set_parameters(parameters)
        self._set_rotation_matrix(transformation)

    def _set_parameters(self, parameters):
        parameter_names = ["centre_y", "centre_z",
                           "semi_axis_y", "semi_axis_z"]
        self.parameters = Parameters(zip(parameter_names, parameters))

    def centre(self):
        return vector.Three(0.0,
                            self.parameters.centre_y,
                            self.parameters.centre_z)

    def _set_rotation_matrix(self, transformation):
        # Rotate pi/2 about the y-axis.
        self.rotation = _np.matrix([[ 0,  0, -1],
                                    [ 0,  1,  0],
                                    [ 1,  0,  0]])

    def crude_extent(self):
        return max(map(abs, self.parameters))

    def gdml_solid(self):
        return _pygdml.solid.EllipticalTube(self.name,
                                            self.parameters.semi_axis_z,
                                            self.parameters.semi_axis_y,
                                            0.5 * self._scale)


class YEC(Body):
    """
    An infinite elliptical cylinder parallel to the y-axis.

    Parameters:

    centre_z (Az) - z-coordinate of the centre of the ellipse face.
    centre_x (Ax) - x-coordinate of the centre of the ellipse face.
    semi_axis_z (Lz) - semi-axis in the z-direction of the ellipse face.
    semi_axis_x (Lx) - semi-axis in the x-direction of the ellipse face.
    """
    def __init__(self, name,
                 parameters,
                 translation=None,
                 transformation=None):
        super(YEC, self).__init__(name,
                                  translation,
                                  transformation)
        self._set_parameters(parameters)
        self._set_rotation_matrix(transformation)

    def _set_parameters(self, parameters):
        parameter_names = ["centre_z", "centre_x",
                           "semi_axis_z", "semi_axis_x"]
        self.parameters = Parameters(zip(parameter_names, parameters))

    def centre(self):
        return vector.Three(self.parameters.centre_x,
                            0.0,
                            self.parameters.centre_z)

    def _set_rotation_matrix(self, transformation):
        # Rotate by pi/2 about the x-axis.
        self.rotation = _np.matrix([[ 1,  0,  0],
                                    [ 0,  0,  1],
                                    [ 0, -1,  0]])

    def crude_extent(self):
        return max(map(abs, self.parameters))

    def gdml_solid(self):
        return _pygdml.solid.EllipticalTube(self.name,
                                            self.parameters.semi_axis_x,
                                            self.parameters.semi_axis_z,
                                            0.5 * self._scale)


class ZEC(Body):
    """
    An infinite elliptical cylinder parallel to the z-axis.

    Parameters:

    centre_x (Ax) - x-coordinate of the centre of the ellipse face.
    centre_y (Ay) - y-coordinate of the centre of the ellipse face.
    semi_axis_x (Lx) - semi-axis in the x-direction of the ellipse face.
    semi_axis_y (Ly) - semi-axis in the y-direction of the ellipse face.
    """
    def __init__(self, name,
                 parameters,
                 translation=None,
                 transformation=None):
        super(ZEC, self).__init__(name,
                                  translation,
                                  transformation)
        self._set_parameters(parameters)
        self._set_rotation_matrix(transformation)

    def _set_parameters(self, parameters):
        parameter_names = ["centre_x", "centre_y",
                           "semi_axis_x", "semi_axis_y"]
        self.parameters = Parameters(zip(parameter_names, parameters))

    def centre(self):
        return vector.Three(self.parameters.centre_x,
                            self.parameters.centre_y,
                            0.0)

    def _set_rotation_matrix(self, transformation):
        self.rotation = _np.matrix(_np.identity(3))

    def crude_extent(self):
        return max(map(abs, self.parameters))

    def gdml_solid(self):
        return _pygdml.solid.EllipticalTube(self.name,
                                            self.parameters.semi_axis_x,
                                            self.parameters.semi_axis_y,
                                            0.5 * self._scale)


class Region(object):
    """
    Class used for interfacing a Fluka region with a GDML volume.
    This class has the underlying pygdml volume payload, alongside its
    placement and rotation in the world volume, and a material.

    """
    def __init__(self, name, zones, material="G4_Galactic"):
        self.name = name
        self.material = material
        if isinstance(zones, list):
            self.zones = dict(zip(range(len(zones)),
                                  zones))
        elif isinstance (zones, Zone):
            self.zones = {0: zones}
        else:
            raise TypeError("Unkown zones type: {}".format(type(zones)))

    def view(self, zones=None, setclip=True, optimise=False):
        """
        View this single region.  If a null mesh is encountered, try
        the view_debug method to see the problematic boolean operation.

        """
        w = _pygdml.solid.Box("world", 10000, 10000, 10000)
        world_volume = _pygdml.Volume([0, 0, 0], [0, 0, 0], w,
                                      "world-volume", None,
                                      1, False, "G4_NITROUS_OXIDE")
        solid = self.evaluate(zones, optimise=optimise)
        solid.add_to_volume(world_volume)
        if setclip is True:
            world_volume.setClip()
        mesh = world_volume.pycsgmesh()
        viewer = _pygdml.VtkViewer()
        viewer.addSource(mesh)
        viewer.view()

    def add_to_volume(self, volume, zones=None, optimise=True):
        """
        Basically for adding to a world volume.

        """
        boolean = self.evaluate(zones, optimise=optimise)
        # Convert the matrix to TB xyz:
        rotation_angles = _trf.matrix2tbxyz(boolean.rotation)
        # Up to this point all rotations are active, which is OK
        # because so are boolean rotations.  However, volume rotations
        # are passive, so reverse the rotation:
        rotation_angles = _trf.reverse(rotation_angles)
        _pygdml.volume.Volume(rotation_angles,
                              boolean.centre(),
                              boolean.gdml_solid(),
                              self.name,
                              volume,
                              1,
                              False,
                              self.material)

    def evaluate(self, zones=None, optimise=True):
        zones = self._select_zones(zones)
        # Get the boolean solids from the zones:
        booleans = [zone.evaluate(optimise=optimise) for zone in zones]
        out_boolean = reduce(or_, booleans)
        return out_boolean

    def _select_zones(self, zones):
        if zones is None:
            zones = self.zones.values()
        elif isinstance(zones, list):
            zones = [self.zones[key] for key in zones]
        else:
            raise TypeError("Unknown zone selection type: ".format(type(zones)))
        return zones

    def extent(self, zones=None):
        boolean = self.evaluate(zones)
        return boolean._extent()


class Zone(object):
    """
    Class representing a Zone (subregion delimited by '|'), i.e. a
    tract of space to be unioned with zero or more other zones.  A
    Zone may also have sub-zones (which in this implementation are
    simply nested Zone instances.

    Parameters
    ----------

    pairs: list of tuplestuples of the form (operator, Body) or
           (operator, SubZone), where operator is a string of the form
           '+' or '-'.

    """

    def __init__(self, pairs):
        self.contains = []
        self.excludes = []
        if isinstance(pairs, tuple):
            self._add_space(pairs[0], pairs[1])
        elif isinstance(pairs, list):
            for operator, body in pairs:
                self._add_space(operator, body)
        else:
            raise TypeError("Unknown pairs type: {}".format(type(pairs)))

        if not self.contains:
            raise TypeError("Zone must always contain at least"
                            " one body or subzone!!!")

    def _add_space(self, operator, body):
        """
        Add a body or SubZone to this region.

        """
        if not isinstance(body, (Body, Zone)):
            raise TypeError("Unknown body type: {}".format(type(body)))

        if operator == '+':
            self.contains.append(body)
        elif operator == '-':
            self.excludes.append(body)
        else:
            raise TypeError("Unknown operator: {}".format(operator))

    @classmethod
    def from_lists(cls, contains, excludes):
        no_contains = len(contains)
        no_excludes = len(excludes)

        return cls((zip(no_contains * ['+'], contains)
                    + zip(no_excludes * ['-'], excludes)))

    def __repr__(self):
        contains_bodies = ' '.join([('+{}').format(space.name)
                                    for space in self.contains if
                                    isinstance(space, Body)])
        excludes_bodies = ' '.join([('-{}').format(space.name)
                                    for space in self.excludes if
                                    isinstance(space, Body)])
        contains_zones = ' '.join(['+({})'.format(repr(space))
                                   for space in self.contains if
                                   isinstance(space, Zone)])
        excludes_zones = ' '.join(['-({})'.format(repr(space))
                                   for space in self.excludes if
                                   isinstance(space, Zone)])
        return "{} {}{}{}".format(contains_bodies,
                                 excludes_bodies,
                                 contains_zones,
                                 excludes_zones)

    def crude_extent(self):
        extent = 0.0
        for body in self.contains + self.excludes:
            extent = max(extent, body.crude_extent())
        return extent

    def _accumulate_intersections(self, first, second):
        pass

    def view(self, setclip=True, optimise=True):
        self.evaluate(optimise=optimise).view(setclip=setclip)

    def evaluate(self, optimise=False):
        """
        Evaluate the zone, returning a Boolean instance with the
        appropriate optimisations, if any.

        """
        if optimise:
            return self._optimised_boolean()
        else:
            return self._crude_boolean()

    def _crude_boolean(self):
        scale = self.crude_extent() * 10.
        # Map the crude extents to the solids:
        self._map_extent_2_bodies(self.contains, scale)
        self._map_extent_2_bodies(self.excludes, scale)

        return self._evaluate()

    def _optimised_boolean(self):
        out = self._crude_boolean()
        # Rescale the bodies and zones with the resulting mesh:
        self._map_extent_2_bodies(self.contains, out)
        boolean_from_ints = reduce(add, self.contains)
        self._map_extent_2_bodies(self.excludes, boolean_from_ints)

        return self._evaluate()

    def _map_extent_2_bodies(self, bodies, extent):
        for body in bodies:
            if isinstance(body, Body):
                body.resize(extent)
            elif isinstance(body, Zone):
                body._map_extent_2_bodies(body.contains, extent)
                body._map_extent_2_bodies(body.excludes, extent)

    def _evaluate(self):
        # This is where the bodies and subzones are condensed to a
        # single Boolean and returned.  Calling this function is
        # dependent on the extents/scales being set for this zones's
        # bodies and subzones, hence why it is hidden.
        accumulated = None # An intersection with None is just self..
        for body in self.contains:
            if isinstance(body, Body):
                accumulated = body.intersect(accumulated)
            elif isinstance(body, Zone):
                accumulated = body._evaluate().intersect(accumulated)

        for body in self.excludes:
            if isinstance(body, Body):
                accumulated = accumulated.subtract(body)
            elif isinstance(body, Zone):
                accumulated = accumulated.subtract(body._evaluate())
        return accumulated

    def extent(self):
        boolean = self.evaluate(optimise=False)
        return boolean._extent()


class Boolean(Body):
    def __init__(self, name, solid, centre, rotation):
        self.name = name
        self._solid = solid
        self._centre = centre
        self.rotation = rotation

    def gdml_solid(self):
        return self._solid

    def centre(self):
        return self._centre

    def view_debug(self, first=None, second=None):
        w = _pygdml.solid.Box("world", 10000, 10000, 10000)
        world_volume = _pygdml.Volume([0, 0, 0], [0, 0, 0], w,
                                      "world-volume", None,
                                      1, False, "G4_NITROUS_OXIDE")
        self.add_to_volume(world_volume)
        try:
            world_volume.pycsgmesh()
            print "Mesh was successful."
        except _pygdml.solid.NullMeshError as error:
            print error.message
            print "Debug:  Viewing consituent solids."
            self._view_null_mesh(error, first, second, setclip=False)

    def _view_null_mesh(self, error, first, second, setclip=False):
        solid1 = error.solid.obj1
        solid2 = error.solid.obj2
        tra2 = error.solid.tra2

        world_box = _pygdml.solid.Box("world", 10000, 10000, 10000)
        world_volume = _pygdml.Volume([0, 0, 0], [0, 0, 0], world_box,
                                      "world-volume", None,
                                      1, False, "G4_NITROUS_OXIDE")
        if (first is None and second is None
            or first is True and second is True):
            volume1 = _pygdml.Volume([0, 0, 0], [0, 0, 0], solid1,
                                     solid1.name, world_volume,
                                     1, False, "G4_NITROUS_OXIDE")
            volume2 = _pygdml.Volume(_trf.reverse(tra2[0]), tra2[1], solid2,
                                     solid2.name, world_volume,
                                     1, False, "G4_NITROUS_OXIDE")
        elif first is True and second is not True:
            volume1 = _pygdml.Volume([0, 0, 0], [0, 0, 0], solid1,
                                     solid1.name, world_volume,
                                     1, False, "G4_NITROUS_OXIDE")
        elif second is True and first is not True:
            volume2 = _pygdml.Volume(_trf.reverse(tra2[0]), tra2[1], solid2,
                                     solid2.name, world_volume,
                                     1, False, "G4_NITROUS_OXIDE")
        elif first is False and second is False:
            raise RuntimeError("Must select at least one"
                               " of the two solids to view")
        if setclip is True:
            world_volume.setClip()
        mesh = world_volume.pycsgmesh()
        viewer = _pygdml.VtkViewer()
        viewer.addSource(mesh)
        viewer.view()

    def gdml_primitives(self):
        # quick and dirty..  revisit this at a later date.
        primitives = []
        def primitive_iter(solid):
            if isinstance(solid, (_pygdml.solid.Intersection,
                                  _pygdml.solid.Subtraction,
                                  _pygdml.solid.Union)):
                primitives.append(primitive_iter(solid.obj1))
                primitives.append(primitive_iter(solid.obj2))
            else:
                primitives.append(solid)
        primitive_iter(self.gdml_solid())
        return [primitive for primitive in primitives
                if primitive is not None]

class Parameters(object):
    # Kind of rubbishy class but sufficient for what it's used for (a
    # very rudimentary mutable record-type class)
    def __init__(self, parameters):
        self._fields = []
        for parameter, value in parameters:
            setattr(self, parameter, value)
            self._fields.append(parameter)

    def __repr__(self):
        out_string = ', '.join(['{}={}'.format(parameter,
                                               getattr(self, parameter))
                                for parameter in self._fields])
        return "Parameters:({})".format(out_string)

    def __iter__(self):
        for field_name in self._fields:
            yield getattr(self, field_name)


class Extent(object):
    def __init__(self, lower, upper):
        try:
            lower.x
            self.lower = lower
        except AttributeError:
            self.lower = vector.Three(lower)
        try:
            upper.x
            self.upper = upper
        except AttributeError:
            self.upper = vector.Three(upper)
        try:
            size = upper - lower
            centre = upper - 0.5 * size
        except TypeError:
            size = [upper[i] - lower[i] for i, _ in enumerate(upper)]
            centre =  [upper[i] - 0.5 * size[i] for i, _ in enumerate(upper)]
        self.size = size
        self.centre = centre

    @classmethod
    def from_wv(cls, wv):
        """Construct an Extent object from a pygdml (world) volume instance. """
        mesh = wv.pycsgmesh()
        extent =  _pygdml.volume.pycsg_extent(mesh)
        lower = vector.Three(extent[0].x, extent[0].y, extent[0].z)
        upper = vector.Three(extent[1].x, extent[1].y, extent[1].z)
        size = upper - lower
        centre = upper - size / 2
        return cls(lower, upper)

    def is_close_to(self, other):
        return bool((_np.isclose(self.lower, other.lower).all()
                     and _np.isclose(self.upper, other.upper).all()))

    def __repr__(self):
        return ("Extent: Lower({lower.x}, {lower.y}, {lower.z}),"
                " Upper({upper.x}, {upper.y}, {upper.z})".format(
                    upper=self.upper, lower=self.lower))

code_meanings = {
    "ARB": "Abitrary Convex Polyhedron",
    "BOX": "General Rectangular Parallelepiped",
    "ELL": "Elippsoid of Revolution",
    "PLA": "Generic Infinite Half-space",
    "QUA": "Generic Quadric",
    "RAW": "Right Angle Wedge",
    "RCC": "Right Circular Cylinder",
    "REC": "Right Ellitpical Cylinder",
    "RPP": "Rectangular Parallelepiped",
    "SPH": "Sphere",
    "TRC": "Truncated Right Angle Cone",
    "WED": "Right Angle Wedge",
    "XCC": "Infinite Circular Cylinder parallel to the x-axis",
    "XEC": "Infinite Elliptical Cylinder parallel to the x-axis",
    "XYP": "Infinite Half-space perpendicular to the z-axis",
    "XZP": "Infinite Half-space perpendicular to the y-axis",
    "YCC": "Infinite Circular Cylinder parallel to the y-axis",
    "YEC": "Infinite Elliptical Cylinder parallel to the y-axis",
    "YZP": "Infinite Half-space perpendicular to the x-axis",
    "ZCC": "Infinite Circular Cylinder parallel to the z-axis",
    "ZEC": "Infinite Elliptical Cylinder parallel to the z-axis"
}
