# bikepathparse.py

import lxml.etree

# Bike path type weighting
# Weights reflecting the relative impact of different bike path types.
# These weights are relatively arbitrary and may be adjusted via some trial and error.
weights = {'MultiUseTrail':1.0,
            'BikeBlvd':0.75,
            'BikeCrossing':0.6,
            'BikeLane':0.5,
            'Null':0.5,
            'WideRoad': 0.2,
            'BikeRoute':0.1}

# KML namespace
kmlns = '{http://earth.google.com/kml/2.2}'

def bikepathparse(filename):
    '''Parse KML bike paths file and return path list of dictionaries with lists of coordinate points and metadata.'''

    # Parse KML file
    bptree = lxml.etree.parse(filename)

    # Extract all path elements
    pcoords = bptree.findall('//'+kmlns+'coordinates')

    # Reformat each path into a set of lat/long coordinates as floats, dropping altitude (zero anyway)
    paths = []
    for pcoord in pcoords:
        paths += [[map(float,x.split(',')[:2]) for x in pcoord.text.split()]]

    # Extract all metadata elements
    mds = bptree.findall('//'+kmlns+'description')

    # Build dictionary with path coordinates and metadata
    bpaths = []

    for i in range(len(pcoords)):
        # Extract path type, name, and length (miles) from embedded HTML and add path weight
        ptype,pname,plen = lxml.html.fromstring(mds[i].text).text_content().split('\n\n')[5:-2][0::2]
        if ptype == '&lt;Null&gt;':
            ptype = 'Null'
        
        bpaths += [{'type':ptype,'name':pname,'length':plen,'coordinates':paths[i],'weight':weights[ptype]}]

    return bpaths


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
