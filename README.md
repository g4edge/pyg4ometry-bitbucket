pyg4ometry Copyright (c) Royal Holloway, University of London 2015 - 2022

General Information
===================

Stewart Boogert       <stewart.boogert@rhul.ac.uk> (main contact)  
Andrey Abramov        <andrey.abramov.2012@live.rhul.ac.uk>  
Laurie Nevay          <laurie.nevay@rhul.ac.uk>  
Will Shields          <william.shields.2010@live.rhul.ac.uk>  
Stuart Walker         <Stuart.Walker.2011@live.rhul.ac.uk>

Installation Guide
==================

  * Required libraries VTK, CGAL, pybind11, opencascade
  * Optional libraries ROOT, USD
  * Install from pypi (pip install pyg4ometry)
  * Install from source (git clone https://stewartboogert@bitbucket.org/jairhul/pyg4ometry.git; cd pyg4ometry; make install or make develop)
  * Mac ports deps (cgal5, opencascade, boost, cmake, python3X)
  * Mac brew deps (cgal, opencascade, cmake, python3X)
  * Ubuntu deps (cgal, opencascade (V7_5_1) from source and patched, cmake, python3X)

Installation Guide Container
============================
 
Build the docker container

  * cd pyg4ometry/docker/
  * docker build --build-arg PYG4OMETRY_VER=0 -t centos-pyg4ometry -f Dockerfile-centos-pyg4ometry .

If the *pyg4ometry* `git` repository has changed change the value of PYG4OMETRY_VER variable
as this will for a clone and install 

Run an image (here is my script for Mac and Docker Desktop)

  * export ip=`(ifconfig en0 | grep inet | awk '$1 == "inet" {print $2}')`
  * xhost +$ip
  * docker run -ti -v /tmp/.X11-unix:/tmp/.X11-unix -v /Users/sboogert/Physics:/tmp/Physics -e DISPLAY=$ip:0 centos-bdsim 
  
Documentation 
=============

Main online manual can be found at http://www.pp.rhul.ac.uk/bdsim/pyg4ometry/

To build manual within this repository:

  * cd pyg4ometry/docs/
  * make html
  * open build/html/index.html


Issues, bugs and feature requests 
=================================

  * For bug reports please use the bitbucket issue trackers

https://bitbucket.org/jairhul/pyg4ometry/issues

Citation and Academic Credit 
============================

  * It pyg4ometry has been useful for your work, please in the first instance cite [Computer Physics Communications Volume 272, March 2022, 108228](https://www.sciencedirect.com/science/article/pii/S0010465521003404)