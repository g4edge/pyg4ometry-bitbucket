import pyg4ometry 

def makeSquare(sizex = 1, sizey = 1, offset = 0):
	pa = pyg4ometry.pycgal.Polygon_2.Polygon_2_EPECK()
	p1 = pyg4ometry.pycgal.Point_2.Point_2_EPECK(0,0)+offset
	p2 = pyg4ometry.pycgal.Point_2.Point_2_EPECK(0,sizey)+offset
	p3 = pyg4ometry.pycgal.Point_2.Point_2_EPECK(sizex,sizey)+offset
	p4 = pyg4ometry.pycgal.Point_2.Point_2_EPECK(sizex,0)+offset

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

def test_polygon_2_difference_hole():
	pa = makeSquare(5,5,pyg4ometry.pycgal.Vector_2.Vector_2_EPECK(0.0,0.0))
	pb = makeSquare(2,2,pyg4ometry.pycgal.Vector_2.Vector_2_EPECK(1,1))

	pr = pyg4ometry.pycgal.Polygon_with_holes_2.List_Polygon_with_holes_2_EPECK()

	pyg4ometry.pycgal.CGAL.difference(pa,pb,pr)

	return pr

def test_polygon_2_difference_hole_2():
	pa = test_polygon_2_difference_hole()[0]
	pb = makeSquare(1,10,pyg4ometry.pycgal.Vector_2.Vector_2_EPECK(2,-3))

	pr = pyg4ometry.pycgal.Polygon_with_holes_2.List_Polygon_with_holes_2_EPECK()

	pyg4ometry.pycgal.CGAL.difference(pa,pb,pr)

	return pr
