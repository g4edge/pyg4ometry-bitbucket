#!/usr/bin/env python
from sys import argv
zeroth = ("* Description goes here\n")
first = ("TITLE\n")
second = ("GEOBEGIN               1.0E-04"
          "                           1.0          COMBNAME\n")
third = "    0    0                   MC-CAD\n"
fourth = "* Bodies go here!\n"
fifth = "END\n"
sixth = "* regions go here\n"
seventh = "END\n"
eighth = "GEOEND\n"
ninth = "* Materials go here\n"
tenth = ("MATERIAL         6.0                 1.8"
         "                              GRAPHITE\n")
eleventh = ("ASSIGNMA    GRAPHITE    REGION_NAME\n")



if __name__ == "__main__":
    name = argv[1]

    with open(name, 'w') as out:
        out.writelines([zeroth,
                        first,
                        second,
                        third,
                        fourth,
                        fifth,
                        sixth,
                        seventh,
                        eighth,
                        ninth,
                        tenth,
                        eleventh])
