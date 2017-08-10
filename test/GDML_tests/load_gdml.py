#!/usr/bin/env python

"""
This script loads a GDML file and visualises it in PYGEOMETRY

Options:
-------------------------------------------------------------------------------------------
|filename    | --filename | The path to the GDML file to be loaded                        |
-------------------------------------------------------------------------------------------
|interactive | -i         | When enabled an interactive IPython session is launched after |
|            |            | visualisation window is closed.                               |
-------------------------------------------------------------------------------------------

Example: ./load_gdml.py --filename=Par02/Par02FullDetector_geant4parsed.gdml -i
"""

import os as _os
import optparse as _optparse
import pygeometry.gdml as _gdml
import pygeometry.geant4 as _geant4
import pygeometry.vtk as _vtk
import pkgutil as _pkgutil
try:
    import IPython as _ipython
    found_ipython = True
except:
    found_ipython = False 


def Load(filename, interactive=False):

    if not filename:
        print "No file specified. Terminating."
        return

    if _os.path.isfile(filename) and filename[-5:] == ".gdml":
        fname, dpath = _stripFilepath(filename, verbose=1)
    else:
        print filename
        raise IOError('Missing file or invalid file format, GDML file (.gdml) required')

    _os.chdir(dpath)

    reader   = _gdml.Reader(fname)
    registry = _geant4.registry
    worldvol = registry.worldVolume
    meshlist = worldvol.pycsgmesh()
    
    vis      =  _vtk.Viewer()
    vis.addPycsgMeshList(meshlist)
    vis.view()

    if interactive:
        if found_ipython:
            _ipython.embed()
        else:
            print "No IPython installed, cannot use interactive mode."


def _stripFilepath(filepath, verbose=False):
    cwd        = _os.getcwd()
    path       = filepath.split("/")
    filename   = path[-1]                         #last element is the filename

    if(path[0]=="/"):                             #when absolute filepath is given
        dirpath = path[:-1]
    elif(path[0]=="." and path[1]=="/"):          #when ./ is used to specify current folder
        path=path[1:]
        dirpath = cwd+"/".join(path[:-1])
    else:
        dirpath = cwd+"/"+"/".join(path[:-1])  #when relative filepath is given

    if verbose:
        print "Filename: ",filename
        print "Directory: ",dirpath

    return filename, dirpath
    

def Main():
    usage = ''
    parser = _optparse.OptionParser(usage)
    parser.add_option('-f','--filename',     action='store',     dest="filename",  type="string", default="")
    parser.add_option('-i','--interactive',  action='store_true',default=False)

    options,args = parser.parse_args()

    if args:
        print "ERROR when parsing, leftover arguments", args
        raise SystemExit

    Load(options.filename, options.interactive)


if __name__ == "__main__":
    Main()
