.. _cli-interface:

======================
Command Line Interface
======================

pyg4ometry provides a command line interface that it can be used by rather than starting python
and using the various classes and methods.

It can be used like: ::

  pyg4ometry --help


This will produce the instructions:

.. code-block:: text

  Usage: pyg4ometry [options]

  Options:
  -h, --help            show this help message and exit
  -v, --view            view geometry
  -b, --bounding        calculate bounding box
  -a, --analysis        geometry information
  -c, --checkoverlaps   check overlaps
  -n, --nullmesh        disable null mesh exception
  -p PLANECUTTER, --planeCutter=PLANECUTTER
                        add (p)plane cutter -p x,y,z,nx,ny,nz
  -P CUTTERFILE, --planeCutterOutput=CUTTERFILE
                        plane cutter output file
  -I INFO, --info=INFO  information on geometry (tree, reg, instance)
  -i INFILE, --file=INFILE
                        (i)nput file (gdml, stl, inp, step)
  -o OUTFILE, --output=OUTFILE
                        (o)utout file (gdml, inp, usd, vtp)
  -d COMPAREFILE, --compare=COMPAREFILE
                        comp(a)re geometry
  -l LVNAME, --logical=LVNAME
                        extract logical LVNAME
  -e APPENDFILE, --append=APPENDFILE
                        app(e)nd geometry
  -x LVNAME, --exchange=LVNAME
                        replace solid for logical volume, LVNAME is logical
                        volume name
  -C, --clip            clip to mother world solid. Or exchanged solid if
                        specified
  -s PYTHONSOLID, --solid=PYTHONSOLID
                        solid in python constructor syntax (used with
                        exchange). Registry must be reg and _np used for numpy
  -t X,Y,Z, --translation=X,Y,Z
                        translation x,y,z (used with append/exchange)
  -r TX,TY,TZ, --rotation=TX,TY,TZ
                        rotation (Tait-Bryan) tx,ty,tz (used with
                        append/exchange)
  -m MATERIAL, --material=MATERIAL
                        material dictionary ("lvname":"nist")
  -f FEATUREDATA, --feature=FEATUREDATA
                        feature extraction from simple geometry
                        (planeQuality,circumference)
  -F FEATUREFILE, --featureExtractOutput=FEATUREFILE
                        feature extract output
  -V, --verbose         verbose script
  -S SCALE, --gltfScale=SCALE
                        scale factor for gltf conversion
