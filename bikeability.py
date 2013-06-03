#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

# bikedata2json.py

# Read in zone and path data. Output bikeability data in JSON for further processing and visualization.

import json
import sys

import folium

import pandas as pd

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

    geojson_tmpl = {'type': 'Feature',
                    'id': None, # will be square no.
                    'properties': {}, # various properties (numbers of paths, etc)
                    'geometry': {} }

    # Output data structure
    out_ds = []
    
    for s in squares:
        num_paths = s[1]

        # If no paths in a square, avoid outputting any data for it
        if num_paths < 1:
            continue

        t = geojson_tmpl.copy()
        t['id'] = s[0]

        properties = {}
        properties['paths'] = num_paths
        properties['pathsnorm'] = s[1]/float(maxcount)
        t['properties'] = properties

        coordinates = s[2]
                                           
        polygon_feature = {'type': 'Polygon',
                           'coordinates': [] }
        polygon_feature['coordinates'] = [coordinates]
        t['geometry'] = polygon_feature

        out_ds.append(t)

    ofile.write(json.dumps(out_ds, indent=4, separators=(',', ': ')))
    ofile.close()
    
def genmap(geojsonfile, mapfile):
    '''Generate HTML map of Albuquerque and city squares using GeoJSON data.'''
    
    geojson = json.load(open(geojsonfile))
    
    # Build pandas dataframe of zone bike path "densities"
    pandas_indexes = []
    pandas_series = []
    for g in geojson:
        pandas_indexes.append(g['id'])
        pandas_series.append({'label': g['id'],
                              'paths': g['properties']['paths'],
                              'pathsnorm': g['properties']['pathsnorm']})
                              
    df = pd.DataFrame(pandas_series, index=pandas_indexes)
    
    # Create map
    abq_centerpoint = [35.0841034, -106.6509851]
    map = folium.Map(location=abq_centerpoint, tiles='Stamen Toner')
    map.geo_json(geo_path=geojsonfile, data_out='data.json', data=df,
                 columns=['label', 'paths'],
                 key_on='feature.id',
                 fill_color='YlGn', fill_opacity=0.5, line_opacity=0.2)
    map.create_map(path=mapfile)

        
def main():
    if len(sys.argv) < 3:
        print("Try running me with: ./%s BikePaths.kmz zoneatlaspagegrid.kmz out.json" % sys.argv[0])
        sys.exit(1)

    bikepathfile = open(sys.argv[1])
    zonefile = open(sys.argv[2])
    json_path = sys.argv[3]

    bikedata2json(bikepathfile, zonefile, json_path)
    
    genmap(json_path, 'map.html')

if __name__ == '__main__':
    main()
