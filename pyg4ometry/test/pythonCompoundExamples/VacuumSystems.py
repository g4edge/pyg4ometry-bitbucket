import os as _os
from os import path as _path
import numpy as _np
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi
import pyg4ometry.transformation as _tr
import pyg4ometry.convert as _convert
import pyg4ometry.fluka as _fluka
import pyg4ometry.visualisation as _vis

lengthSafety = 1e-5

def CF_BlankFlange(name = "flange1", cf_dn = 'DN16', reg = None, vis=True, write=True) :

    if reg == None :
        reg = _g4.Registry()

    # https://en.wikipedia.org/wiki/Vacuum_flange
    # https://www.leyboldproducts.com/media/pdf/8e/c6/3f/CP_080_Fittings_EN57beb2d4b36d0.pdf

    cf_data = {'DN16': {'outerDiameter':34,'innerDiameter':16,'innerDiameter1':21.3,'holeCircleDiameter':27,
                        'holeNumber':6,'holeDiameter':4.3,'height':7.5,'height1':1.4},
               'DN40': {'outerDiameter':69.5, 'innerDiameter':36.8, 'innerDiameter1':48.1, 'holeCircleDiameter': 58.7,
                        'holeNumber':6, 'holeDiameter':6.6, 'height':13.0, 'height1':1.4},
               'DN63': {'outerDiameter':113.5, 'innerDiameter':66.0, 'innerDiameter1':82.4,'holeCircleDiameter':92.2,
                        'holeNumber':8, 'holeDiameter':8.4, 'height':17.5, 'height1':1.4},
               'DN100': {'outerDiameter':152.0, 'innerDiameter':104.0, 'innerDiameter1':120.5, 'holeCircleDiameter':130.3,
                        'holeNumber':16, 'holeDiameter':8.4, 'height': 20.0, 'height1': 1.4},
               'DN160': {'outerDiameter':202.5, 'innerDiameter':155.0, 'innerDiameter1':171.3, 'holeCircleDiameter':181.0,
                        'holeNumber':20, 'holeDiameter':8.4, 'height': 22.0, 'height1':1.4},
               'DN200': {'outerDiameter':253.0, 'innerDiameter':200.0, 'innerDiameter1':222.1, 'holeCircleDiameter':231.8,
                        'holeNumber':24, 'holeDiameter':8.4, 'height':24.5, 'height1':1.4},
               'DN250': {'outerDiameter':305.0, 'innerDiameter':250.0, 'innerDiameter1':272.7, 'holeCircleDiameter':284.0,
                        'holeNumber':32, 'holeDiameter':8.4, 'height': 24.5, 'height1':1.4}}

    data = cf_data[cf_dn]

    flangeSolid = _g4.solid.Tubs(name+"_flange",0,data['outerDiameter']/2.0,
                                 data['height'],0,"2*pi",reg,"mm","rad")

    # subtract bolt holes
    dPhi = 2*_np.pi/data['holeNumber']
    for i in range(0,data['holeNumber'],1) :
        holeSolid   = _g4.solid.Tubs(name+"_hole_"+str(i),0,data['holeDiameter']/2.0,data['height']*1.05,0,"2*pi",reg,"mm","rad")

        x = data['holeCircleDiameter']/2.0*_np.cos(i*dPhi)
        y = data['holeCircleDiameter']/2.0*_np.sin(i*dPhi)

        flangeSolid = _g4.solid.Subtraction(name+"_sub_"+str(i),flangeSolid,holeSolid,[[0,0,0],[x,y,0]],reg)

    cfSolid     = _g4.solid.Tubs(name+"_cf",0,data['innerDiameter1']/2.0,data['height1'],0,"2*pi",reg,"mm","rad")
    flangeSolid = _g4.solid.Subtraction(name + "_sub_" + str(data['holeNumber']), flangeSolid, cfSolid, [[0, 0, 0], [0, 0, data['height']/2]], reg)

    flangeMaterial = _g4.MaterialPredefined("G4_STAINLESS-STEEL")
    flangeLogical  = _g4.LogicalVolume(flangeSolid, flangeMaterial, name+"Logical", reg)

    # set world volume
    reg.setWorld(flangeLogical.name)

    # gdml output
    if write :
        w = _gd.Writer()
        w.addDetector(reg)
        w.write(_os.path.join(_os.path.dirname(__file__), "CF_Flange.gdml"))

    if vis :
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view()

    return {'logical':flangeLogical, 'length':data['height']}

def CF_BeamPipe(name, bpLength = 500, bpId = 30, bpThickness = 2.5, flange1 = 'DN40', flange2 = 'DN40',
                reg = None, vis = True, write = False) :

    if reg == None :
        reg = _g4.Registry()

    bpSolid      = _g4.solid.Tubs(name+"_bp",bpId/2,bpId/2+bpThickness,bpLength,0,"2*pi",reg,"mm","rad")
    bpSolidInner = _g4.solid.Tubs(name+"_bpInner",0,bpId/2,bpLength,0,"2*pi",reg,"mm","rad")

    length = bpLength

    # make first flange
    if flange1 != None :
        flange1      = CF_BlankFlange(name+"flange1",flange1,reg=reg, vis=False)
        flange1Solid = flange1['logical'].solid

        # cut through flange
        flange1Solid = _g4.solid.Subtraction(flange1Solid.name+"_cut",flange1Solid,bpSolidInner,[[0,0,0],[0,0,0]],reg)

        # union with beam pipe
        bpSolid = _g4.solid.Union(name+"_bp_flange1", bpSolid,flange1Solid,
                                  [[0,_np.pi,0],[0,0,-bpLength/2+flange1['length']/2]],reg)

        length += flange1['length']

    # add second flange
    if flange2 != None :
        flange2      = CF_BlankFlange(name+"flange2",flange2,reg=reg,vis=False)
        flange2Solid = flange2['logical'].solid

        # cut through flange
        flange2Solid = _g4.solid.Subtraction(flange2Solid.name+"_cut",flange2Solid,bpSolidInner,[[0,0,0],[0,0,0]],reg)

        # union with beam pipe
        bpSolid = _g4.solid.Union(name+"_bp_flange2", bpSolid, flange2Solid,
                                  [[0,0,0], [0,0,bpLength/2-flange2['length']/2]], reg)

        length += flange2['length']

    bpMaterial = _g4.MaterialPredefined("G4_STAINLESS-STEEL")
    bpLogical  = _g4.LogicalVolume(bpSolid, bpMaterial, name+"Logical", reg)

    # set world volume
    reg.setWorld(bpLogical.name)

    # gdml output
    if write :
        w = _gd.Writer()
        w.addDetector(reg)
        w.write(_os.path.join(_os.path.dirname(__file__), "CF_BeamPipe.gdml"))

    if vis :
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view()


    extent = bpLogical.extent(True)

    return {'logical':bpLogical, 'length':length, 'innerSolid':bpSolidInner}


def CF_CylindiricalChamber(name):
    pass

def CF_CuboidalChamber(name):
    pass

def CF_SphericalChamber(name, innerRadius = 100, outerRadius = 107,
                        ports = {'port1':{'rotn':[0,         0,0], 'id':30, 'thickness':5, 'length':100, 'flange':'DN40', 'term':'DN40'},
                                 'port2':{'rotn':[0,_np.pi/2.0,0], 'id':30, 'thickness':5, 'length':150, 'flange':'DN40', 'term':'DN40'},
                                 'port3':{'rotn':[_np.pi/2.0,0,0], 'id':30, 'thickness':5, 'length':200, 'flange':'DN40', 'term':'DN40'},
                                 'port4':{'rotn':[-_np.pi/4.0,-_np.pi/4.0, 0],'id':10,'thickness':2.5, 'length':200, 'flange':'DN16', 'term':'DN16'},
                                 'port5':{'rotn':[-3*_np.pi/4.0,-3*_np.pi/4.0, 0],'id':10,'thickness':2.5, 'length':100, 'flange':'DN16', 'term':'DN16'}
                                 },
                        reg = None, vis = False, write = False) :

    if reg == None :
        reg = _g4.Registry()

    chamberSolid      = _g4.solid.Sphere(name+"_sphere",innerRadius,outerRadius,0,"2*pi",0,"pi",reg)
    chamberCutSolid   = _g4.solid.Orb(name+"_sphereInner",innerRadius,reg)

    # loop over ports
    for k in ports :
        port      = ports[k]
        rotn      = port['rotn']
        length    = port['length']
        id        = port['id']
        thickness = port['thickness']
        flange    = port['flange']
        term      = port['term']

        bp = CF_BeamPipe(name+"_"+k, bpLength=length,bpId=id, bpThickness=thickness, flange1=None,flange2=flange,reg=reg,vis=False)

        bpSolid      = bp['logical'].solid
        bpCutSolid   = _g4.solid.Tubs(bpSolid.name+"_cut",0,id/2,2*(outerRadius-innerRadius),0,"2*pi",reg,"mm","rad")

        bpSolid    = _g4.solid.Subtraction(bpSolid.name+"_sub1",bpSolid,chamberCutSolid,
                                           [[0,0,0],[0,0,-outerRadius]],reg)

        pos  = list(_tr.tbxyz2matrix(rotn).dot(_np.array([0,0,outerRadius])))
        pos1 = list(_tr.tbxyz2matrix(rotn).dot(_np.array([0,0,outerRadius-(outerRadius-innerRadius)])))

        chamberSolid = _g4.solid.Subtraction(chamberSolid.name+"_sub1",chamberSolid,bpCutSolid,
                                             [rotn,pos1],reg)
        chamberSolid = _g4.solid.Union(chamberSolid.name+"_uni1",chamberSolid,bpSolid,
                                       [rotn,pos],reg)

    chamberMaterial = _g4.MaterialPredefined("G4_STAINLESS-STEEL")
    chamberLogical  = _g4.LogicalVolume(chamberSolid, chamberMaterial, "chamberLogical", reg)

    # set world volume
    reg.setWorld(chamberLogical.name)

    extent = chamberLogical.extent(True)

    # gdml output
    if write :
        w = _gd.Writer()
        w.addDetector(reg)
        w.write(_os.path.join(_os.path.dirname(__file__), "CF_SphericalChamber.gdml"))

    if vis :
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view()

    return {'logical':chamberLogical}


def Test(vis = True, interactive = False):

    reg = _g4.Registry()

    chamber = CF_SphericalChamber("test1", vis=False,reg=reg)
    #chamber = CF_BeamPipe("test1",reg=reg)
    #chamber   = CF_BlankFlange("test1",reg=reg)

    log = chamber['logical']
    extent = log.extent(True)

    # create world box
    ws = _g4.solid.Box("worldSolid",
                       2*(extent[1][0]-extent[0][0]),
                       2*(extent[1][1]-extent[0][1]),
                       2*(extent[1][2]-extent[0][2]),
                       reg,"mm")

    wm = _g4.MaterialPredefined("G4_Galactic")

    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    cp = _g4.PhysicalVolume([_np.pi/4.0,0,0],[0,0,0], log, "chamber_pv1", wl, reg)

    reg.setWorld(wl.name)

    # test extent of physical volume
    extentBB = wl.extent(includeBoundingSolid=True)

    ################################
    # visualisation
    ################################
    v = None
    if vis :
        v = _vis.VtkViewer()
        v.addLogicalVolume(wl)
        v.setOpacity(0.25)
        v.view(interactive=interactive)

    ################################
    # export as obj
    ################################
    _vis.pycsgMeshToObj(log.mesh.localmesh,_path.join(_path.dirname(__file__),"SphericalChamber"))

    ################################
    # write gdml
    ################################
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_path.join(_path.dirname(__file__),"SphericalChamber.gdml"))

    ################################
    # write fluka
    ################################
    freg = _convert.geant4Logical2Fluka(wl)

    w = _fluka.Writer()
    w.addDetector(freg)
    w.write(_path.join(_os.path.dirname(__file__),"SphericalChamber.inp"))

    # flair output file
    f = _fluka.Flair("SphericalChamber.inp",extentBB)
    f.write(_path.join(_path.dirname(__file__),"SphericalChamber.flair"))