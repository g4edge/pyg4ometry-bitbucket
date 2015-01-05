#include "carve/geom.hpp"
#include "carve/mesh.hpp"
#include "carve/matrix.hpp"
#include "carve/input.hpp"
#include "carve/csg.hpp"

carve::mesh::MeshSet<3> *makeCube(const carve::math::Matrix &transform);
carve::mesh::MeshSet<3> *makeCylinder(int iSlices, double dRadius, double dHeight, const carve::math::Matrix &transform);
carve::mesh::MeshSet<3> *makeTruncatedCone(const carve::math::Matrix &transform);
carve::mesh::MeshSet<3> *makeSphere(int iLat, int iLong, const carve::math::Matrix &transform);
carve::mesh::MeshSet<3> *makePlane(const carve::math::Matrix &transform);
carve::mesh::MeshSet<3> *makeWedge(const carve::meth::Matrix &transform);
carve::mesh::MeshSet<3> *makeQuadric(const carve::math::Matrix &transform);
