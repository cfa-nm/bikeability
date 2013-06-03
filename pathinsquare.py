# pathinsquare.py

# Determine how many bike paths have intersected a given square mile of the city.
# In which we throw optimization to the wind.

import matplotlib.nxutils as nx # Deprecated as of matplotlib 1.2.0, use matplotlib.path instead and related functions
from math import sqrt

def insertpoints(path):
    '''Insert extra points in path for long spans between points to increase chance of detection that they intersect square.'''
    
    # Estimated mile in degrees in Albuquerque. Accuracy is not very important here.
    mile = 0.0145
    threshold = mile/1.0
    
    # Insert points as needed. Adjust loop imax accordingly.
    i = 0
    imax = len(path) - 1
    while i < imax:
        if dist(path[i],path[i+1]) < threshold:
            path = path[:i+1] + [splitpoints(path[i],path[i+1])] + path[i+1:]
            i += 2
            imax += 1
        else:
            i += 1
            
    return path
    
def dist(p1,p2):
    '''Calculate distance between two points.'''
    
    distance = sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
    
    return distance

def splitpoints(p1,p2):
    '''Return a point halfway between the given points.'''
    
    dx = abs(p1[0]-p2[0])/2.0
    dy = abs(p1[1]-p2[1])/2.0
    
    if p1[0] < p2[0]:
        x = p1[0] + dx
    else:
        x = p2[0] + dx
        
    if p1[1] < p2[1]:
        y = p1[1] + dy
    else:
        y = p2[1] + dy
    
    return [x,y]
    
    
def pathtally(paths,square):
    '''Tally the number of paths that intersect the given square.'''
    
    tally = 0
    
    for path in paths:
        for point in path:
            if nx.pnpoly(point[0],point[1],square[:-1]):
                tally += 1
                break
    
    return tally
    
def pathinsquare(paths,squares):
    '''Process paths and squares. Returning list of squares with count of intersecting paths.'''
    
    paths = [insertpoints(path) for path in paths]
    
    squares = [[name,pathtally(paths,square),square] for name,square in squares]
    
    return squares
    
