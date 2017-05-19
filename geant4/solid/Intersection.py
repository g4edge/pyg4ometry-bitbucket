from SolidBase import SolidBase as _SolidBase
from pygeometry.geant4.Registry import registry as _registry
from pygeometry.transformation import *
import copy as _copy

class Intersection(_SolidBase) :
    """
    name = name
    obj1 = unrotated, untranslated solid
    obj2 = solid rotated and translated according to tra2
    tra2 = [rot,tra]
         = [[a,b,g],[dx,dy,dz]]
    """
    def __init__(self, name, obj1, obj2, tra2):
        self.type = "booli"
        self.name = name
        self.obj1 = obj1
        self.obj2 = obj2
        self.tra2 = tra2
        self.mesh = None
        _registry.addSolid(self)

    def __repr__(self):
        return 'Intersection : ('+str(self.obj1)+') n ('+str(self.obj2)+')'

    def pycsgmesh(self):

        print 'Intersection' \
              '' \
              ' ',self.name, self.obj1.name, self.obj2.name

        if self.mesh : 
            return self.mesh

        rot   = tbxyz(self.tra2[0])
        tlate = self.tra2[1]

        m1 = self.obj1.pycsgmesh()
        m2 = _copy.deepcopy(self.obj2.pycsgmesh()) # need top copy this mesh as it is transformed
        m2.rotate(rot[0],rad2deg(rot[1]))
        m2.translate(tlate)
        self.obj2mesh = m2

        self.mesh = m1.intersect(m2)
        if not self.mesh.toPolygons():
            print 'Intersection null mesh',self.name,self.obj1.name, m1, self.obj2.name, m2
            raise NullMeshError(self)

        self.obj1.mesh = None
        self.obj2.mesh = None

        print 'intersection mesh ', self.name
        return self.mesh

    def gdmlWrite(self,w) :
        oe  = w.doc.createElement('intersection')
        oe.setAttribute('name',self.name)
        cfe = w.doc.createElement('first')
        cfe.setAttribute('ref',self.obj1.name)
        w.solids.appendChild(cfe)
        
        cse = doc.createElement('second')
        cse.setAttribute('ref',self.obj2.name)
        w.solids.appendChild(cse)

        csce = doc.createElement('positionref')
        csce.setAttribute('ref',self.name+'_sol2_pos')
        oe.appendChild(csce)
        
        csce1 = doc.createElement('rotationref')
        csce1.setAttribute('ref', self.name + '_sol2_rot')
        oe.appendChild(csce1)
        
        p = doc.createElement('position')
        p.setAttribute('name',cs.name+'_sol2_pos')
        p.setAttribute('x',str(cs.tra2[1][0]))
        p.setAttribute('y',str(cs.tra2[1][1]))
        p.setAttribute('z',str(cs.tra2[1][2]))
        de.appendChild(p)
        
        r = self.doc.createElement('rotation')
        r.setAttribute('name',cs.name + '_sol2_rot')
        r.setAttribute('x', str(cs.tra2[0][0]))
        r.setAttribute('y', str(cs.tra2[0][1]))
        r.setAttribute('z', str(cs.tra2[0][2]))
        de.appendChild(r)
        

