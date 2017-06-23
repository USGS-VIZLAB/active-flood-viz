from flask import request, render_template, abort
from svgis import svgis

from . import app
from . import maputils


@app.route('/home/')
def home():
    # This program requires svgis to be installed (which in turn requires Fiona and GDAL)
    # Takes a list of site ids and bounding info in config file
    # Creates an svg

    site_list = app.config['SITE_IDS']
    bounds = app.config['BOUNDS']
    # cities = app.config['CITIES']


    # TODO: move function to utils

    # list of dicts
    data_nice = maputils.site_dict(site_list, app.config['NWIS_SITE_SERVICE_ENDPOINT'])


    # write data to gages.json
    maputils.write_geojson("floodviz/static/data/gages.json", data_nice)

    # write map and store in x
    x = svgis.map(("floodviz/static/data/counties.json", "floodviz/static/data/gages.json",
                   "floodviz/static/data/cities.json"), bounds=bounds, crs="epsg:2794", scale=300)

    # write map to mapout.svg
    # with open("floodviz/static/data/mapout.svg", "w") as f:
    #     f.write(x)

    return render_template('index.html', x=x)



