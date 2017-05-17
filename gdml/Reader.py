import pygeometry.geant4 as _g4
import pygeometry.vtk    as _vtk
#import pygeometry.gdml   as _gdml
import numpy             as _np
from xml.dom import minidom as _minidom
import warnings as _warnings
from math import pi as _pi

class Reader :
    def __init__(self, filename) :
        self.filename = filename

        self.constants        = {}
        self.positions        = {}
        self.quantities       = {}
        self.rotations        = {}
        self.worldVolumeName  = str()
        self.exclude          = [] #parametrized volumes not converted

        # load file
        self.load()


    def load(self):
        data  = open(self.filename)
        #remove all newline charecters and whitespaces outside tags
        fs = str()
        for l in data:
            l = l.strip()
            if(l.endswith(">")):
                end=""
            else:
                end=" "
            if(len(l) != 0):
                fs += (l+end) 

        xmldoc = _minidom.parseString(fs)

        self.parseDefines(xmldoc)
        self.parseSolids(xmldoc)
        self.parseStructure(xmldoc)
        

    def parseDefines(self, xmldoc):
        self.structure = xmldoc.getElementsByTagName("define")[0]

        for df in self.structure.childNodes :
            try :
                define_type  = df.tagName
            except AttributeError :
                # comment so continue
                continue

            name         = df.attributes["name"].value
            attrs        = df.attributes

            keys       = attrs.keys()
            vals       = [attr.value for attr in attrs.values()]
            def_attrs  = {key: val for (key,val) in zip(keys, vals)}

            if(define_type == "constant"):
                self.constants[name]=df.attributes["value"].value
            elif(define_type == "position"):
                self.positions[name]=self._getCoordinateList(def_attrs)
            elif(define_type == "quantity"):
                self.quantities[name] =self._get_var("value", float, "atr", **def_attrs)
            elif(define_type == "rotation"):
                self.rotations[name] = self._getCoordinateList(def_attrs)
            else:
                print "Urecognised define: ", define_type
                
    def parseSolids(self, xmldoc):
        solids_list = [] 
        self.xmlsolids = xmldoc.getElementsByTagName("solids")[0]

        for sd in self.xmlsolids.childNodes :
            csg_solid_types = ["subtraction", "union", "intersection"]
            ply_solid_types = ["polycone", "polyhedra"]
            solid_type = sd.tagName
            
            if (solid_type in csg_solid_types): #need to inspect child nodes to get all parameters for csg solids
                keys = sd.attributes.keys()
                vals = [attr.value for attr in sd.attributes.values()]

                for csgsd in sd.childNodes:
                    prm = csgsd.tagName
                    if(prm == "first" or prm == "second"):
                        keys.append(prm)
                        vals.append(csgsd.attributes["ref"].value)
                    elif(prm == "position" or prm == "rotation"):
                        pos_keys = csgsd.attributes.keys()
                        pos_vals = [attr.value for attr in csgsd.attributes.values()]
                        pos = {key: val for (key,val) in zip(pos_keys, pos_vals)}
                        keys.append(prm)
                        vals.append(pos)

                    else:
                        _warnings.warn("CSG solid paramets '"+prm+"' unknown")

                gdml_attributes = {key: val for (key,val) in zip(keys, vals)}

            elif (solid_type in ply_solid_types): #need to inspect child nodes to get zplane info for poly solids
                keys = sd.attributes.keys()
                vals = [attr.value for attr in sd.attributes.values()]

                rmin  = []
                rmax  = []
                z     = []

                count = 0                         #counter is used to mangle the key and make it unique for every z plane
                for zplane in sd.childNodes:
                    tagname = zplane.tagName
                    if(tagname == "zplane"):      #check that its not some other type of child node
                        keys_zpl = zplane.attributes.keys()
                        vals_zpl = [attr.value for attr in zplane.attributes.values()]
                        keys_zpl = [key+"_"+str(count) for key in keys_zpl] #keep track of different z planes and allow looping
                        keys.extend(keys_zpl)
                        vals.extend(vals_zpl)
                        count = count+1

                    else:
                        _warnings.warn("Poly-solid tag '"+tagname+"' unknown")

                keys.append("nzplanes")
                vals.append(count)
                
                gdml_attributes = {key: val for (key,val) in zip(keys, vals)}

            elif (solid_type == "xtru"):     #the extrusion solid is a special case
                keys = sd.attributes.keys()
                vals = [attr.value for attr in sd.attributes.values()]

                count_vrt = 0
                count_pln = 0
                for xtru_element in sd.childNodes:
                    tagname = xtru_element.tagName
                    if(tagname == "twoDimVertex"):      #check that its not some other type of child node
                        keys_zpl = xtru_element.attributes.keys()
                        vals_zpl = [attr.value for attr in xtru_element.attributes.values()]
                        keys_zpl = [key+"_"+str(count_vrt) for key in keys_zpl] #keep track of different z planes
                        keys.extend(keys_zpl)
                        vals.extend(vals_zpl)
                        count_vrt = count_vrt+1
                        
                    elif(tagname == "section"):      #check that its not some other type of child node
                        keys_zpl = xtru_element.attributes.keys()
                        vals_zpl = [attr.value for attr in xtru_element.attributes.values()]
                        number   = int(xtru_element.attributes["zOrder"].value)
                        keys_zpl = [key+"_"+str(number) for key in keys_zpl] #keep track of different z planes
                        keys.extend(keys_zpl)
                        vals.extend(vals_zpl)
                        count_pln = count_pln+1
                    else:
                        _warnings.warn("Extrusion solid tag '"+tagname+"' unknown")

                keys.append("nzplanes")
                vals.append(count_pln)
                keys.append("nverts")
                vals.append(count_vrt)
                
                gdml_attributes = {key: val for (key,val) in zip(keys, vals)}

            else:
                keys       = sd.attributes.keys()
                vals       = [attr.value for attr in sd.attributes.values()]
                gdml_attributes = {key: val for (key,val) in zip(keys, vals)}
            
            solid = self._constructCSGSolid(solid_type, gdml_attributes)
            
            #if(solid is not None):
            #    self.solids[sd.attributes["name"].value] = solid
                
        
    def parseStructure(self, xmldoc):

        # find structure
        self.structure = xmldoc.getElementsByTagName("structure")[0]

        # loop over structure child nodes
        for chNode in self.structure.childNodes :
            self._extractNodeData(chNode)

        # find world logical volume
        self.setup  = xmldoc.getElementsByTagName("setup")[0]
        worldLvName = self.setup.childNodes[0].attributes["ref"].value
        _g4.registry.orderLogicalVolumes(worldLvName)
        _g4.registry.setWorld(worldLvName)

    def _box(self,**kwargs):
        name = self._get_var("name", str, "atr", **kwargs)
        x    = self._get_var("x", float, "lgt", **kwargs)/2
        y    = self._get_var("y", float, "lgt", **kwargs)/2
        z    = self._get_var("z", float, "lgt", **kwargs)/2

        csgsolid = _g4.solid.Box(name, x, y, z)
        return csgsolid
    

    def _para(self,**kwargs):
        name  = self._get_var("name", str, "atr", **kwargs)
        x     = self._get_var("x", float, "lgt",**kwargs)/2
        y     = self._get_var("y", float, "lgt", **kwargs)/2
        z     = self._get_var("z", float, "lgt", **kwargs)/2
        phi   = self._get_var("phi", float, "ang", **kwargs)
        alpha = self._get_var("alpha", float, "ang", **kwargs)
        theta    = self._get_var("theta", float, "ang", **kwargs)

        csgsolid = _g4.solid.Para(name, x, y, z, alpha, theta, phi)
        return csgsolid

    def _sphere(self,**kwargs):
        name       = self._get_var("name", str, "atr", **kwargs)
        rmin       = self._get_var("rmin", float, "lgt", **kwargs)
        rmax       = self._get_var("rmax", float, "lgt",**kwargs)
        startphi   = self._get_var("startphi", float, "ang",**kwargs)
        deltaphi   = self._get_var("deltaphi", float, "ang",**kwargs)
        starttheta = self._get_var("starttheta", float, "ang",**kwargs)
        deltatheta = self._get_var("rmin", float, "ang", **kwargs)

        csgsolid = _g4.solid.Sphere(name, rmin, rmax, startphi, deltaphi, starttheta, deltatheta)
        return csgsolid

    def _orb(self,**kwargs):
        name = self._get_var("name", str, "atr", **kwargs)
        r    = self._get_var("r", float, "lgt",**kwargs)

        csgsolid = _g4.solid.Orb(name, r)
        return csgsolid

    def _cone(self,**kwargs):
        name  = self._get_var("name", str, "atr", **kwargs)
        rmin1 = self._get_var("rmin1", float, "lgt",**kwargs)
        rmax1 = self._get_var("rmax1", float, "lgt",**kwargs)
        rmin2 = self._get_var("rmin2", float, "lgt",**kwargs)
        rmax2 = self._get_var("rmax2", float, "lgt",**kwargs)
        dz    = self._get_var("z", float, "lgt",**kwargs)/2
        sphi  = self._get_var("startphi", float, "ang",**kwargs)
        dphi  = self._get_var("deltaphi", float, "ang", **kwargs)
        
        csgsolid = _g4.solid.Cons(name, rmin1, rmax1, rmin2, rmax2, dz, sphi, dphi)
        return csgsolid

    def _cutTube(self,**kwargs):
        name  = self._get_var("name", str, "atr", **kwargs)
        rmin  = self._get_var("rmin", float, "lgt",**kwargs)
        rmax  = self._get_var("rmax", float, "lgt",**kwargs)
        dz    = self._get_var("z", float, "lgt",**kwargs)/2
        sphi  = self._get_var("startphi", float, "ang",**kwargs)
        dphi  = self._get_var("deltaphi", float, "ang", **kwargs)
        lx    = self._get_var("lowX", float, "lgt",**kwargs)
        ly    = self._get_var("lowY", float, "lgt",**kwargs)
        lz    = self._get_var("lowZ", float, "lgt",**kwargs)
        hx    = self._get_var("highX", float, "lgt",**kwargs)
        hy    = self._get_var("highY", float, "lgt",**kwargs)
        hz    = self._get_var("highZ", float, "lgt",**kwargs)
        lNorm = [lx, ly, lz]
        hNorm = [hx, hy, hz]
        
        csgsolid = _g4.solid.CutTubs(name, rmin, rmax, dz, sphi, dphi, lNorm, hNorm)
        return csgsolid

    def _ellipsoid(self,**kwargs):
        name  = self._get_var("name", str, "atr", **kwargs)
        ax    = self._get_var("ax", float, "lgt", **kwargs)
        ay    = self._get_var("ay", float, "lgt", **kwargs)
        az    = self._get_var("az", float, "lgt", **kwargs)
        bcut  = self._get_var("zcut1", float, "lgt", **kwargs)
        tcut  = self._get_var("zcut2", float, "lgt", **kwargs)
        
        csgsolid = _g4.solid.Ellipsoid(name, ax, ay, az, bcut, tcut)
        return csgsolid

    def _trd(self,**kwargs):
        name = self._get_var("name", str, "atr",**kwargs)
        x1   = self._get_var("x1", float, "lgt",**kwargs)/2
        x2   = self._get_var("x2", float, "lgt",**kwargs)/2
        y1   = self._get_var("y1", float, "lgt",**kwargs)/2
        y2   = self._get_var("y2", float, "lgt",**kwargs)/2
        z    = self._get_var("z", float, "lgt",**kwargs)/2

        csgsolid = _g4.solid.Trd(name, x1, x2, y1, y2, z)
        return csgsolid

    def _torus(self,**kwargs):
        name  = self._get_var("name", str, "atr",**kwargs)
        rmin  = self._get_var("rmin", float, "lgt",**kwargs)
        rmax  = self._get_var("rmax", float, "lgt",**kwargs)
        rtor  = self._get_var("rmax", float, "lgt",**kwargs)
        sphi  = self._get_var("startphi",float, "ang", **kwargs)
        dphi  = self._get_var("deltaphi", float, "ang", **kwargs)
        
        csgsolid = _g4.solid.Torus(name, rmin, rmax, rtor, sphi, dphi)
        return csgsolid
    
    def _polyhedra(self,**kwargs):
        name     = self._get_var("name", str, "atr",**kwargs)
        sphi     = self._get_var("startphi",float, "ang", **kwargs)
        dphi     = self._get_var("deltaphi", float, "ang", **kwargs)
        nsides   = self._get_var("numsides", int, "atr", **kwargs)
        nzpl     = self._get_var("nzplanes", int, "atr", **kwargs)

        Rmin = []
        Rmax = []
        Z    = []
        for i in range(nzpl):
            rmin     = self._get_var("rmin_"+str(i), float, "lgt",**kwargs)
            rmax     = self._get_var("rmax_"+str(i), float, "lgt",**kwargs)
            z        = self._get_var("z_"+str(i), float, "lgt",**kwargs)
            Rmin.append(rmin)
            Rmax.append(rmax)
            Z.append(z)
            
        csgsolid = _g4.solid.Polyhedra(name, sphi, dphi, nsides, nzpl, Z, Rmin, Rmax)
        return csgsolid

    def _xtru(self,**kwargs):
        name    = self._get_var("name", str, "atr",**kwargs)

        nzpl    = self._get_var("nzplanes", int, "atr", **kwargs)
        nvrt    = self._get_var("nverts", int, "atr", **kwargs)

        verts   = []
        zplanes = []

        for i in range(nvrt):
            x     = self._get_var("x_"+str(i), float, "lgt",**kwargs)
            y     = self._get_var("y_"+str(i), float, "lgt",**kwargs)
            vert = [x,y]
            verts.append(vert)
        
        for i in range(nzpl):
            zpos      = self._get_var("zPosition_"+str(i), float, "lgt",**kwargs)
            xoffs     = self._get_var("xOffset_"+str(i), float, "lgt",**kwargs)
            yoffs     = self._get_var("yOffset_"+str(i), float, "lgt",**kwargs)
            scl       = self._get_var("scalingFactor_"+str(i), float, "atr",**kwargs)

            zplane = [zpos,[xoffs,yoffs], scl]
            zplanes.append(zplane)
            
        csgsolid = _g4.solid.ExtrudedSolid(name, verts, zplanes)
        return csgsolid
    
    def _tube(self,**kwargs):
        name  = self._get_var("name", str, "atr", **kwargs)
        rmin  = self._get_var("rmin", float, "lgt",**kwargs)
        rmax  = self._get_var("rmax", float, "lgt",**kwargs)
        sphi  = self._get_var("startphi",float, "ang", **kwargs)
        dphi  = self._get_var("deltaphi", float, "ang", **kwargs)
        z     = self._get_var("z", float, "lgt", **kwargs)/2

        csgsolid = _g4.solid.Tubs(name, rmin, rmax, z, sphi, dphi)
        return csgsolid

    def _subtraction(self,**kwargs):
        name     = kwargs.get("name")
        first    = kwargs.get("first")
        second   = kwargs.get("second")
        pos_dict = kwargs.get("position", {})
        rot_dict = kwargs.get("rotation", {})

        try:                                   #if both inital solids are not correctly constructed this will fail
            first_solid  = _g4.registry.solidDict[first]
            second_solid = _g4.registry.solidDict[second]

            x_rot = self._get_var("x", float, "ang", **rot_dict)
            y_rot = self._get_var("y", float, "ang", **rot_dict)
            z_rot = self._get_var("z", float, "ang", **rot_dict)
            
            x_pos = self._get_var("x", float, "lgt", **pos_dict)
            y_pos = self._get_var("y", float, "lgt", **pos_dict)
            z_pos = self._get_var("z", float, "lgt", **pos_dict)
            
            transform = [[x_rot, y_rot, z_rot],[x_pos, y_pos, z_pos]]
        
            csgsolid = _g4.solid.Subtraction(name, first_solid, second_solid, transform)

        except:
            csgsolid = None
            
        return csgsolid
    
    def _union(self,**kwargs):
        name     = kwargs.get("name")
        first    = kwargs.get("first")
        second   = kwargs.get("second")
        pos_dict = kwargs.get("position", {})
        rot_dict = kwargs.get("rotation", {})

        try:                                   #if both inital solids are not correctly constructed this will fail
            first_solid  = _g4.registry.solidDict[first]
            second_solid = _g4.registry.solidDict[second]

            x_rot = self._get_var("x", float, "ang", **rot_dict)
            y_rot = self._get_var("y", float, "ang", **rot_dict)
            z_rot = self._get_var("z", float, "ang", **rot_dict)
            
            x_pos = self._get_var("x", float, "lgt", **pos_dict)
            y_pos = self._get_var("y", float, "lgt", **pos_dict)
            z_pos = self._get_var("z", float, "lgt", **pos_dict)
            
            transform = [[x_rot, y_rot, z_rot],[x_pos, y_pos, z_pos]]
        

            csgsolid = _g4.solid.Union(name, first_solid, second_solid, transform)

        except:
            csgsolid = None
            
        return csgsolid

    def _intersection(self,**kwargs):
        name     = kwargs.get("name")
        first    = kwargs.get("first")
        second   = kwargs.get("second")
        pos_dict = kwargs.get("position", {})
        rot_dict = kwargs.get("rotation", {})

        try:                                   #if both inital solids are not correctly constructed this will fail
            first_solid  = _g4.registry.solidDict[first]
            second_solid = _g4.registry.solidDict[second]

            x_rot = self._get_var("x", float, "ang", **rot_dict)
            y_rot = self._get_var("y", float, "ang", **rot_dict)
            z_rot = self._get_var("z", float, "ang", **rot_dict)
            
            x_pos = self._get_var("x", float, "lgt", **pos_dict)
            y_pos = self._get_var("y", float, "lgt", **pos_dict)
            z_pos = self._get_var("z", float, "lgt", **pos_dict)
        
            transform = [[x_rot, y_rot, z_rot],[x_pos, y_pos, z_pos]]
        

            csgsolid = _g4.solid.Intersection(name, first_solid, second_solid, transform)

        except:
            csgsolid = None
            
        return csgsolid


    def _constructCSGSolid(self, solid_type, attributes):
        """
        Constructs a Pycsg Solid from the attributes of a GDML solid.
        
        Inputs:
          attributes: dictionary of parameters for the solid
        
        Returns:
          Instance of one of the solids supported by pygdml or None
          if the solid is not supported
        """
        supported_solids = {"box": self._box, "para": self._para, "tube": self._tube, "cone": self._cone, "ellipsoid": self._ellipsoid,
                            "polyhedra": self._polyhedra, "torus": self._torus, "xtru": self._xtru, "cutTube": self._cutTube, 
                            "trd":self._trd, "sphere":self._sphere, "orb": self._orb, "subtraction": self._subtraction,
                             "intersection": self._intersection, "union": self._union}

        st = solid_type
        if st in supported_solids.keys():
            solid = supported_solids[st](**attributes)
            if(solid is not None):
                pass
            else:
                "Solid construction failed: "+st+" "+attributes["name"]
            return solid
        else:
            print "Solid "+st+" not supported, abort construction"


    def _get_var(self, varname, var_type, param_type, **kwargs):

        if(var_type == int):   #inputs are all stings so set defaults to proper type
            default = 0
        elif(var_type == float):
            default = 0.0
        elif(var_type == str):
            default = ""

        #search for the absolute value
        try:
            var = var_type(kwargs.get(varname, default))    #get attribute value if attribute is present

        except(ValueError):                                 #if attribute found, but typecasting fails, search defines to check if its referenced
            try:
                var = var_type(self.quantities[kwargs.get(varname, default)])
            except(KeyError):                               #if attribute value is not found in defined quantities, look in constants
                try:
                    var = eval(self.constants[kwargs.get(varname, default)])
                    #print varname," ",kwargs.get(varname, default)," ",var
                except(KeyError):
                    _warnings.warn("Variable "+varname+" not found")
                    var = None

        #convert units where neccessary
        if var is not default:
            if("unit" in kwargs):
                uts = kwargs["unit"]
            elif("aunit" in kwargs and param_type=="ang"):
                uts = kwargs["aunit"]
            elif("lunit" in kwargs and param_type=="lgt"):
                uts = kwargs["lunit"]
            else:
                uts = "default"
        else:
            uts = "default"

        var = self._toStandUnits(var,uts)

        return var

    def _getCoordinateList(self, kwargs):
        x = self._get_var("x", float, "atr", **kwargs)
        y = self._get_var("y", float, "atr", **kwargs)
        z = self._get_var("z", float, "atr", **kwargs)

        return [x,y,z]

    def _extractNodeData(self, node):
        node_name = node.tagName
        
        if node.nodeType == node.ELEMENT_NODE:
            if(node_name == "volume"):
                name      = node.attributes["name"].value
                material  = node.getElementsByTagName("materialref")[0].attributes["ref"].value
                solid     = node.getElementsByTagName("solidref")[0].attributes["ref"].value
                daughters = [] #done elsewhere
                vol       = _g4.LogicalVolume(_g4.registry.solidDict[solid], material, name)
                
                for chNode in node.childNodes :
                    if chNode.tagName == "physvol" : 
                        volref    = chNode.getElementsByTagName("volumeref")[0].attributes["ref"].value
                        position  = self._evalCoordRef(chNode, "position")
                        rotation  = self._evalCoordRef(chNode, "rotation")
                        scale     = self._evalCoordRef(chNode, "scale")
                        physvol   = _g4.PhysicalVolume(rotation, position, _g4.registry.logicalVolumeDict[volref],
                                                       chNode.attributes["name"].value,vol,scale)
                        
                
                    elif(node_name == "paramvol"):
                        print "Volume ", node.parentNode.attributes["name"].value, "excluded - parametrised volume" #debug
                        volref  = node.getElementsByTagName("volumeref")[0].attributes["ref"].value
                        self.exclude.append(volref)                                                 #TODO: include parametrised solids
                        """
                        ncopies   = node.attributes["ncopies"].val
                        volref    = node.getElementsByTagName("volumeref")[0].attributes["ref"].value
                        for in range(1, ncopies):
                        position  = self._evalCoordRef(node, "position")
                        rotation  = self._evalCoordRef(node, "rotation")
                        mother    = node.parentNode.attributes["name"].value
                        self.gdmlphvols[volref] = [mother, position, rotation]
            
                        print volref," ",position," ", rotation #DEBUG
                        """
            else:
                print "Unrecognised node", nodename
                
    def _evalCoordRef(self, node, coordstype): #TODO(aabramov): optimise fetching of parameters using self.get_var
       
        try:
            if(coordstype == "rotation"):
                aslist = self.rotations[node.getElementsByTagName("rotationref")[0].attributes["ref"].value] #coordinate conversion is done at reading for member dicts
            elif(coordstype == "position"):
                aslist = self.positions[node.getElementsByTagName("positionref")[0].attributes["ref"].value]
            elif(coordstype == "scale"):
                aslist = self.positions[node.getElementsByTagName("scaleref")[0].attributes["ref"].value]
            else:
                _warnings.warn("Invalid coordinate type "+coordstype+". Valid types are 'position' and 'rotation'")
                aslist=None
        except(IndexError):
            try:
                if(coordstype == "position"):
                    crd = node.getElementsByTagName(coordstype)[0]
                    try:
                        uts = crd.attributes["unit"].value
                    except(KeyError):
                        uts = "default"
                        
                    x   = self._toStandUnits(float(crd.attributes["x"].value), uts)
                    y   = self._toStandUnits(float(crd.attributes["y"].value), uts)
                    z   = self._toStandUnits(float(crd.attributes["z"].value), uts)
                    aslist = [x,y,z]

                elif(coordstype == "rotation"):
                    crd = node.getElementsByTagName(coordstype)[0]
                    try:
                        uts = crd.attributes["unit"].value
                    except(KeyError):
                        uts = "default"
                        
                    x   = self._toStandUnits(float(crd.attributes["x"].value), uts)
                    y   = self._toStandUnits(float(crd.attributes["y"].value), uts)
                    z   = self._toStandUnits(float(crd.attributes["z"].value), uts)
                    aslist = [x,y,z]

                elif(coordstype == "scale"):
                    x = float(node.getElementsByTagName("scale")[0].attributes["x"].value)
                    y = float(node.getElementsByTagName("scale")[0].attributes["y"].value)
                    z = float(node.getElementsByTagName("scale")[0].attributes["z"].value)
                    aslist = [x,y,z]
                    
                else:
                    _warnings.warn("Warning: invalid coordinate type "+coordstype+". Valid types are 'position' and 'rotation'")
                    aslist=None
                    
            except(IndexError):
                if (coordstype == "scale"):
                    aslist=[1.,1.,1.]
                else:
                    aslist = [0.0, 0.0, 0.0]

        return aslist       

    def _toStandUnits(self, value, unit):
        #standard units are mm for length and rad for angle
        multf = {"default":1, "pm":1.e-6, "nm":1.e-3, "mum":1.e-3, "mm":1, "cm":10, "m":1.e3, "deg":2*_pi/360, "rad":1}
        try:
            val = multf[unit]*value #if this fails the value is of unknown unit type
        except:
            return value
        #print val," ",unit," ",val #DEBUG
        
        return val

    def _buildPycsgStructure(self, name, mother, startstring="|", verbose=False):
        solidname  = self.gdmlvols[name][0]
        solid      = self.solids.get(solidname, None)
        material   = self.gdmlvols[name][1]
        daughters  = self.gdmlvols[name][2]
        
        phvol_prms = self.gdmlphvols.get(name, [[None,[0.0,0.0,0.0],[0.0,0.0,0.0],[1.,1.,1.], False]]) #the default is the world voume
        for i in range(len(phvol_prms)):

            mother_name = phvol_prms[i][0]
            position    = phvol_prms[i][1]
            rotation    = phvol_prms[i][2]
            scale       = phvol_prms[i][3]
            copyNr      = 0
            checkSurf   = False

                     
            if(solid is not None):                    # TODO: fix the logic here                                                            
                if (mother_name is None):             # world volume special case, no mother
                    volume  = Volume(rotation, position, solid, name,  mother, copyNr, checkSurf, material, scale)
                    self.volumes.append(volume)

                    if(verbose):
                        print "\n==>VOLUME HIREACHY<=="
                        print '{:>4}'.format(str(len(self.volumes))), startstring+name #, " ROT=>",rotation," POS=>",position, " SCL=>",scale
                        startstring = startstring+"    |"                                                                                
                    
                    for daughter in daughters:
                        self._buildPycsgStructure(daughter, volume, startstring=startstring, verbose=verbose)

                    
                elif(mother_name == mother.name): #only place physical volumes if they belong to that logical volume
                    volume  = Volume(rotation, position, solid, name,  mother, copyNr, checkSurf, material, scale)
                    self.volumes.append(volume)

                    if(verbose):
                        print '{:>4}'.format(str(len(self.volumes))), startstring+name #, " ROT=>",rotation," POS=>",position, " SCL=>",scale
                        startstring = startstring+"    |"                                                                                           
                
                    for daughter in daughters:
                        self._buildPycsgStructure(daughter, volume, startstring=startstring, verbose=verbose)
        

