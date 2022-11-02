import pyg4ometry 

def makeSquare(offset):
	pa = pyg4ometry.pycgal.Polygon_2.Polygon_2_EPECK()
	p1 = pyg4ometry.pycgal.Point_2.Point_2_EPECK(0,0)+offset
	p2 = pyg4ometry.pycgal.Point_2.Point_2_EPECK(0,1)+offset
	p3 = pyg4ometry.pycgal.Point_2.Point_2_EPECK(1,1)+offset
	p4 = pyg4ometry.pycgal.Point_2.Point_2_EPECK(1,0)+offset

	pa.push_back(p1)
	pa.push_back(p2)
	pa.push_back(p3)
	pa.push_back(p4)

	return pa


def test_polygon_2_union():
	pa = makeSquare(pyg4ometry.pycgal.Vector_2.Vector_2_EPECK(0.0,0.0))
	pb = makeSquare(pyg4ometry.pycgal.Vector_2.Vector_2_EPECK(0.5,0.5))

	pr = pyg4ometry.pycgal.Polygon_with_holes_2.Polygon_with_holes_2_EPECK()

	pyg4ometry.pycgal.CGAL.join(pa,pb,pr)

	return pr

def test_polygon_2_intersection():
	pa = makeSquare(pyg4ometry.pycgal.Vector_2.Vector_2_EPECK(0.0,0.0))
	pb = makeSquare(pyg4ometry.pycgal.Vector_2.Vector_2_EPECK(0.5,0.5))

	pr = pyg4ometry.pycgal.Polygon_with_holes_2.List_Polygon_with_holes_2_EPECK()

	pyg4ometry.pycgal.CGAL.intersection(pa,pb,pr)

	return pr


def test_polygon_2_difference():
	pa = makeSquare(pyg4ometry.pycgal.Vector_2.Vector_2_EPECK(0.0,0.0))
	pb = makeSquare(pyg4ometry.pycgal.Vector_2.Vector_2_EPECK(0.5,0.5))

	pr = pyg4ometry.pycgal.Polygon_with_holes_2.List_Polygon_with_holes_2_EPECK()

	pyg4ometry.pycgal.CGAL.difference(pa,pb,pr)

	return pr