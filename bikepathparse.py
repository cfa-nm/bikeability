# bikepathparse.py

import lxml.etree

# KML namespace
kmlns = '{http://earth.google.com/kml/2.2}'

def bikepathparse(filename):
    '''Parse KML bike paths file and return list of paths as lists of coordinate points.'''

    # Parse KML file
    bptree = lxml.etree.parse(filename)

    # Extract all path elements
    bps = bptree.findall('//'+kmlns+'coordinates')

    # Reformat each path into a set of lat/long coordinates, dropping altitude (zero anyway)
    paths = []
    for bp in bps:
        paths += [[x.split(',')[:2] for x in bp.text.split()]]
    
    return paths


def zoneparse(filename):
    '''Parse KML zone file and return list of zone name and coordinate points.'''
    
    # Parse KML file
    ztree = lxml.etree.parse(filename)

    # Extract all name and zone boundary elements
    znames = ztree.findall('//'+kmlns+'name')[2:] # Exclude first 2 name elements <-- hack
    znames = [x.text for x in znames] 
    zcoords = ztree.findall('//'+kmlns+'coordinates')

    # Reformat each boundary into a set of lat/long coordinates, dropping altitude (zero anyway)
    # Dropping "redundant" 5th point on square
    bounds = []
    for zcoord in zcoords:
        bounds += [[x.split(',')[:2] for x in zcoord.text.split()][:-1]]  
        
    # Group zone name and boundary coordinates
    zones = zip(znames,bounds)
    
    return zones
