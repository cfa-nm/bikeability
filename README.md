## Bikeability

_Rating the bikeability of Albuquerque neighborhoods_

Using data sourced from the city of Albuquerque and possibly the public, the idea behind _bikeability_ is to rate how bikeable different parts of the city are.

This project will evolve as we go. We are starting with a minimum vision of determining the number of bike lanes / paths / trails / boulevards through each square mile zone of Albuquerque.

We'll see what happens from there.

Data sources:

[ABQ Data](http://www.cabq.gov/abq-data)
* [Bike Paths](http://data.cabq.gov/community/bikepaths/)
* [Zone Atlas](http://data.cabq.gov/business/zoneatlas/)

### Getting up and running

Download both the bike paths data and zone atlas data from the City of Albuquerque's ABQ Data portal, and convert them from KMZ to KML:

    wget http://data.cabq.gov/community/bikepaths/BikePaths.kmz \
         http://data.cabq.gov/business/zoneatlas/zoneatlaspagegrid.kmz
    unzip BikePaths.kmz
    mv doc.kml BikePaths.kml
    unzip zoneatlaspagegrid.kmz
    mv doc.kml zoneatlaspagegrid.kml

setup a virtualenv (recommended) and install requirements:

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
