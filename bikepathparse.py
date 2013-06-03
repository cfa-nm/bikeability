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

    # Reformat each path into a set of lat/long coordinates as floats, dropping altitude (zero anyway)
    paths = []
    for bp in bps:
        paths += [[map(float,x.split(',')[:2]) for x in bp.text.split()]]
    
    return paths


def zoneparse(filename):
    '''Parse KML zone file and return list of zone name and coordinate points.'''
    
    # Parse KML file
    ztree = lxml.etree.parse(filename)

    # Extract all name and zone boundary elements
    znames = ztree.findall('//'+kmlns+'name')[2:] # Exclude first 2 name elements <-- hack
    znames = [x.text for x in znames] 
    zcoords = ztree.findall('//'+kmlns+'coordinates')

    # Reformat each boundary into a set of lat/long coordinates as floats, dropping altitude (zero anyway)
    bounds = []
    for zcoord in zcoords:
        bounds += [[map(float,x.split(',')[:2]) for x in zcoord.text.split()]]  
        
    # Group zone name and boundary coordinates
    zones = zip(znames,bounds)
    
    return zones
