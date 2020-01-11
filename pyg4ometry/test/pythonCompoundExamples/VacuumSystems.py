import os as _os
import numpy as _np
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi


lengthSafety = 1e-5

def CF_BlankFlange(name = "flange1", cf_dn = 'DN16', vis=True, write=True) :

    reg = _g4.Registry()

    # https://en.wikipedia.org/wiki/Vacuum_flange
    # https://www.leyboldproducts.com/media/pdf/8e/c6/3f/CP_080_Fittings_EN57beb2d4b36d0.pdf

    cf_data = {'DN16': {'outerDiameter':34,'innerDiameter':16,'innerDiameter1':21.3,'holeCircleDiameter':27,
                        'holeNumber':6,'holeDiameter':4.3,'height':7.5,'height1':1.4},
               'DN40': {'outerDiameter': 69.5, 'innerDiameter': 36.8, 'innerDiameter1': 48.1, 'holeCircleDiameter': 58.7,
                        'holeNumber': 6, 'holeDiameter': 6.6, 'height': 13.0, 'height1': 1.4},
               'DN63': {'outerDiameter': 113.5, 'innerDiameter': 66.0, 'innerDiameter1': 82.4,
                        'holeCircleDiameter': 92.2,
                        'holeNumber': 8, 'holeDiameter': 8.4, 'height': 17.5, 'height1': 1.4},
               'DN100': {'od': 34, 'id': 16, 'bd': 27, 'h': 7.5, 'nh': 6, 'hd': 4.3},
               'DN160': {'od': 34, 'id': 16, 'bd': 27, 'h': 7.5, 'nh': 6, 'hd': 4.3},
               'DN200': {'od': 34, 'id': 16, 'bd': 27, 'h': 7.5, 'nh': 6, 'hd': 4.3},
               'DN250': {'od': 34, 'id': 16, 'bd': 27, 'h': 7.5, 'nh': 6, 'hd': 4.3}}


    data = cf_data[cf_dn]


    flangeSolid = _g4.solid.Tubs(name+"_flange",0,data['outerDiameter']/2.0,
                                 data['height'],0,"2*pi",reg,"mm","rad")

    # subtract bolt holes

    dPhi = 2*_np.pi/data['holeNumber']

    for i in range(0,data['holeNumber'],1) :
        holeSolid   = _g4.solid.Tubs(name+"_hole_"+str(i),0,data['holeDiameter']/2.0,data['height'],0,"2*pi",reg,"mm","rad")

        x = data['holeCircleDiameter']/2.0*_np.cos(i*dPhi)
        y = data['holeCircleDiameter']/2.0*_np.sin(i*dPhi)

        flangeSolid = _g4.solid.Subtraction(name+"_sub_"+str(i),flangeSolid,holeSolid,[[0,0,0],[x,y,0]],reg)

    cfSolid     = _g4.solid.Tubs(name+"_cf",0,data['innerDiameter1']/2.0,data['height1'],0,"2*pi",reg,"mm","rad")
    flangeSolid = _g4.solid.Subtraction(name + "_sub_" + str(data['holeNumber']), flangeSolid, cfSolid, [[0, 0, 0], [0, 0, data['height']/2]], reg)

    flangeMaterial = _g4.MaterialPredefined("G4_STAINLESS-STEEL")
    flangeLogical  = _g4.LogicalVolume(flangeSolid, flangeMaterial, "flangeLogical", reg)

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
                vis = True, write = False) :

    reg = _g4.Registry()

    bpSolid      = _g4.solid.Tubs(name+"_bp",bpId/2,bpId/2+bpThickness,bpLength,0,"2*pi",reg,"mm","rad")
    bpSolidInner = _g4.solid.Tubs(name+"_bpInner",0,bpId/2,bpLength,0,"2*pi",reg,"mm","rad")


    length = bpLength

    # make first flange
    if flange1 != None :
        flange1      = CF_BlankFlange(name+"flange1",flange1,vis=False)
        flange1Solid = flange1['logical'].solid

        # cut through flange
        flange1Solid = _g4.solid.Subtraction(flange1Solid.name+"_cut",flange1Solid,bpSolidInner,[[0,0,0],[0,0,0]],reg)

        # union with beam pipe
        bpSolid = _g4.solid.Union(name+"_bp_flange1", bpSolid,flange1Solid,
                                  [[0,0,0],[0,0,-bpLength/2-flange1['length']/2 + lengthSafety]],reg)

        length += flange1['length']

    # add second flange
    if flange2 != None :
        flange2      = CF_BlankFlange(name+"flange2",flange2,vis=False)
        flange2Solid = flange2['logical'].solid

        # cut through flange
        flange2Solid = _g4.solid.Subtraction(flange2Solid.name+"_cut",flange1Solid,bpSolidInner,[[0,0,0],[0,0,0]],reg)

        # union with beam pipe
        bpSolid = _g4.solid.Union(name+"_bp_flange2", bpSolid, flange2Solid,
                                  [[0,0,0], [0,0,bpLength/2+flange2['length']/2 - lengthSafety]], reg)

        length += flange2['length']

    bpMaterial = _g4.MaterialPredefined("G4_STAINLESS-STEEL")
    bpLogical  = _g4.LogicalVolume(bpSolid, bpMaterial, "bpLogical", reg)

    # set world volume
    reg.setWorld(bpLogical.name)

    # gdml output
    if write :
        w = _gd.Writer()
        w.addDetector(reg)
        w.write(_os.path.join(_os.path.dirname(__file__), "CF_Flange.gdml"))

    if vis :
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view()

    return {'logical':bpLogical, 'length':length}

def CF_SphericalChamber(name, innerRadius = 300, outerRadius = 310, ports = {}, vis = True, write = False) :

    # port
    # port = {'axis':[0,0,1], 'length':400, 'flange1':'DN40', 'flange2':'DN40', 'term1':'DN40', 'term2':'DN40'}

    reg = _g4.Registry()

    chamberSolid   = _g4.solid.Sphere(name+"_sphere",innerRadius,outerRadius,0,"2*pi",0,"pi",reg)

    # loop over ports
    for k in ports :
        port = ports[k]
        axis = port['axis']
        length = port['length']
        flange1 = port['flange1']
        flange2 = port['flange2']
        term1   = port['term1']
        term2   = port['term2']


    chamberMaterial = _g4.MaterialPredefined("G4_STAINLESS-STEEL")
    chamberLogical  = _g4.LogicalVolume(chamberSolid, chamberMaterial, "chamberLogical", reg)

    # set world volume
    reg.setWorld(chamberLogical.name)

    # gdml output
    if write :
        w = _gd.Writer()
        w.addDetector(reg)
        w.write(_os.path.join(_os.path.dirname(__file__), "CF_Flange.gdml"))

    if vis :
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view()
