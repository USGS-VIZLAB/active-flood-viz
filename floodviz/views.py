from flask import request, render_template, abort
import requests
from svgis import svgis

from . import app


@app.route('/home/')
def home():
    # This program requires svgis to be installed (which in turn requires Fiona and GDAL)
    # Takes a list of site ids and bounding info in config file
    # Creates an svg

    siteList = app.config['SITE_IDS']
    bounds = app.config['BOUNDS']
    # cities = app.config['CITIES']


    # TODO: move function to utils
    # function to generate a dictionary after querying NWIS
    def siteDict(siteList):

        # generate the string of site ids for the url
        id_input_string = ",".join(siteList)

        # create the url
        url = app.config['NWIS_SITE_SERVICE_ENDPOINT'] + "/?format=rdb&sites=" + id_input_string + "&siteStatus=all"

        # get data from url
        data = ""
        req = requests.get(url)
        for line in req.text.splitlines():
            if not line.startswith("#"):
                data += line + '\n'

        # create array by splitting lines
        data = data.split('\n')

        # make a list of dicts  from data
        fields = data[0].split('\t')
        dnice = []
        for line in data[2:]:
            line = line.split('\t')
            line_dict = dict(zip(fields, line))
            dnice.append(line_dict)

        # remove bad element from end of list
        dnice = dnice[:-1]
        return dnice

    # list of dicts
    data_nice = siteDict(siteList)

    # function to write site data to a geojson file
    # TODO: move function to utils
    def writeGeoJson(filename, data):
        with open(filename, "w") as f:
            f.write("{ \"type\": \"FeatureCollection\", \"features\": [ \n")

            count = -1
            for datum in data:
                    count += 1
                    f.write("{ \"type\": \"Feature\",\n \"geometry\": {\n \"type\": \"Point\",\n \"coordinates\" : "
                            "[" + datum.get('dec_long_va') + ", " + datum.get('dec_lat_va') + "]\n },\n")
                    f.write(" \"properties\": {\n \"name\": \"" + datum.get('station_nm') + "\",\n \"id\": \""
                            + datum.get('site_no') + "\",\n \"huc\": \"" +
                            datum['huc_cd'] + "\" \n } \n }")
                    # add a comma unless at end of list
                    if data[count] != data[len(data) - 1]:
                        f.write(",")
                    f.write("\n")
            f.write(" ] }")

    # write data to gages.json
    writeGeoJson("floodviz/static/data/gages.json", data_nice)

    # write map and store in x
    x = svgis.map("floodviz/static/data/gages.json", scale=300, crs="epsg:2794", bounds=bounds)

    # write map to mapout.svg
    # with open("floodviz/static/data/mapout.svg", "w") as f:
    #     f.write(x)

    return render_template('index.html', x=x)



