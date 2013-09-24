# bikepathweight.py

# Assign different weights to different path types.

def pathweight(paths):
    '''Read in path list. Assign different weights to different path types. Return list.'''

    # Weights reflecting the relative impact of different bike path types.
    # These weights are relatively arbitrary and will be adjusted via some trial and error.
    weights = {'MultiUseTrail':1.0,
                'BikeBlvd':0.75,
                'BikeCrossing':0.6,
                'BikeLane':0.5,
                'Null':0.5,
                'WideRoad': 0.2,
                'BikeRoute':0.1}

    for path in paths:
        path['weight'] = weights[path['type']]

    return paths
