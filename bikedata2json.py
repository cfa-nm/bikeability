#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

# bikedata2json.py

# Read in zone and path data. Output bikeability data in JSON for further processing and visualization.

import json
import sys

import bikepathparse
import pathinsquare

def bikedata2json(bikepathfile, zonefile, jsonfile):
    # Get the data in a usable format. Assume you've unzipped the kmz files manually.
    paths = bikepathparse.bikepathparse(bikepathfile)
    squares = bikepathparse.zoneparse(zonefile)
    
    # List formatted squares with tallies of path intersections
    squares = pathinsquare.pathinsquare(paths,squares)
    
    # Determine max path intersection count of any square
    maxcount = max([x[1] for x in squares])
    
    # Write JSON file with square name, path count, normalized count, square boundary coordinates
    ofile = open(jsonfile,'w')

    # Output data structure
    out_ds = []
    
    for s in squares:
        tempdict = {}
        tempdict['Label'] = s[0]
        tempdict['paths'] = s[1]
        tempdict['pathsnorm'] = s[1]/float(maxcount)
        tempdict['coordinates'] = s[2]
        out_ds.append(tempdict)

    ofile.write(json.dumps(out_ds, indent=4, separators=(',', ': ')))
    ofile.close()
        
def main():
    if len(sys.argv) < 3:
        print("Try running me with: ./%s BikePaths.kmz zoneatlaspagegrid.kmz out.json" % sys.argv[0])
        sys.exit(1)

    bikepathfile = open(sys.argv[1])
    zonefile = open(sys.argv[2])

    bikedata2json(bikepathfile, zonefile, sys.argv[3])

if __name__ == '__main__':
    main()
