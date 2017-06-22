import json
import os

from flask import request, render_template, abort
import requests
from svgis import svgis

from . import app


@app.route('/home/')
def home():
    # This program requires svgis to be installed (which in turn requires Fiona and GDAL)
    # Takes a list of site ids in the form of "site_ids.csv" (IDs now given in config file)
    # Takes config data in the form of "site_configs.yaml" (also now given in config file)
    # Takes style in the form of "site_styles.css"
    # Adds a city layer in the form of "cities.json"
    # outputs an SVG with ids for each site

    siteList = app.config['SITE_IDS']
    bounds = app.config['BOUNDS']
    cities = app.config['CITIES']

    # generate the string of site ids for the url

    # TODO: move function to utils
    def siteDict(siteList):
        # generate the string of site ids for the url
        id_input_string = ",".join(siteList)

        url = app.config['NWIS_SITE_SERVICE_ENDPOINT'] + "/?format=rdb&sites=" + id_input_string + "&siteStatus=all"
        print(url)

        # get data from url
        data = ""
        req = requests.get(url)
        for line in req.text.splitlines():
            if not line.startswith("#"):
                data += line + '\n'

        data = data.split('\n')

        # make a nice dictionary from data
        fields = data[0].split('\t')
        dnice = []
        for line in data[2:]:
            line = line.split('\t')
            line_dict = dict(zip(fields, line))
            dnice.append(line_dict)

        dnice = dnice[:-1]
        return dnice

    data_nice = siteDict(siteList)
    # for datum in data_nice:
    #     print(datum)

    # with open("floodviz/static/data/dump.json", "w") as f:
    #     json.dump(data_nice, f)
    # keep only station name, id, huc, lat and lon
    # arr = []

    # store this data in arr
    # for datum in data_nice:
    #     if 'station_nm' in datum.keys():
    #         temp = [datum['station_nm'], datum['site_no'], datum['huc_cd'], datum['dec_lat_va'], datum['dec_long_va']]
    #         arr.append(temp)

    # write data to sites.json in geojson format
    with open("floodviz/static/data/gages.json", "w") as f:
        f.write("{ \"type\": \"FeatureCollection\", \"features\": [ \n")

        count = -1
        for datum in data_nice:
            # if datum.get('agency_cd') == 'USGS':
                count += 1
                f.write("{ \"type\": \"Feature\",\n \"geometry\": {\n \"type\": \"Point\",\n \"coordinates\" : [" + datum.get('dec_long_va') + ", " + datum.get('dec_lat_va') + "]\n },\n")
                f.write(" \"properties\": {\n \"name\": \"" + datum.get('station_nm') + "\",\n \"id\": \"" + datum.get('site_no') + "\",\n \"huc\": \"" +
                        datum['huc_cd'] + "\" \n } \n }")
                if data_nice[count] != data_nice[len(data_nice) - 1]:
                    f.write(",")
                f.write("\n")
        f.write(" ] }")

    x = svgis.map("floodviz/static/data/gages.json", scale=300, crs="epsg:2794", bounds=bounds)

    with open("floodviz/static/data/mapout.svg", "w") as f:
        f.write(x)
    return render_template('index.html')



