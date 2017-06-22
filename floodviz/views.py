from flask import request, render_template, abort
import csv
import requests
import yaml
import os

from . import app


@app.route('/home/')
def home():
    return render_template('index.html')


# This program requires svgis to be installed (which in turn requires Fiona and GDAL)
# Takes a list of site ids in the form of "site_ids.csv" (IDs now given in config file)
# Takes config data in the form of "site_configs.yaml" (also now given in config file)
# Takes style in the form of "site_styles.css"
# Adds a city layer in the form of "cities.json"
# outputs an SVG with ids for each site

siteList = app.config['SITE_IDS']

bounds = app.config['BOUNDS']

# put each site number from the csv into a list
# with open('static/data/site_ids.csv', newline='') as csvfile:
#     siteReader = csv.reader(csvfile)
#     for site in siteReader:
#         if site[0].isalnum():
#             siteList.append(site[0])


# generate the string of site ids for the url
idInputString = ",".join(siteList)
# print(idInputString)

url = "https://waterservices.usgs.gov/nwis/site/?format=rdb&sites=" + idInputString + "&siteStatus=all"

# get data from url
req = requests.get(url)

# Discard preamble from response
data = req.text[req.text.rindex('#') + 1:]
data = data[data.index('\n') + 1:]
# the first line of data is now the column headers

# turn data into list by splitting on \n
data = data.split('\n')

# discard 2nd line
data = [data[0]] + data[2:]

# make a nice dictionary from data
fields = data[0].split('\t')
data_nice = []
for line in data[1:]:
    line = line.split('\t')
    line_dict = dict(zip(fields, line))
    data_nice.append(line_dict)

# keep only station name, id, huc, lat and lon
arr = []

# store this data in arr
for datum in data_nice:
    if 'station_nm' in datum.keys():
        temp = [datum['station_nm'], datum['site_no'], datum['huc_cd'], datum['dec_lat_va'], datum['dec_long_va']]
        arr.append(temp)

# write data to sites.json in geojson format
with open("floodviz/static/data/gages.json", "w") as f:
    f.write("{ \"type\": \"FeatureCollection\", \"features\": [ \n")

    count = -1
    for item in arr:
        count += 1
        f.write("{ \"type\": \"Feature\",\n \"geometry\": {\n \"type\": \"Point\",\n \"coordinates\" : [" + item[
            4] + ", " + item[3] + "]\n },\n")
        f.write(" \"properties\": {\n \"name\": \"" + item[0] + "\",\n \"id\": \"" + item[1] + "\",\n \"huc\": \"" +
                item[2] + "\" \n } \n }")
        if arr[count] != arr[len(arr) - 1]:
            f.write(",")
        f.write("\n")
    f.write(" ] }")

# get bounds from site_configs.yaml
# with open("site_configs.yaml", "r") as stream:
#     bounds_file = yaml.load(stream)
#
# bounds = bounds_file['boundingBox']

# set bounds
bound1 = bounds[0]
bound2 = bounds[1]
bound3 = bounds[2]
bound4 = bounds[3]

# create command string and run svgis from command line
# svgis usage:
# draw [input file]
# -o [output file]
# -f [scale]
# -j [projection]
# -i [geodata field to use as id]
# -c [css file]
# -b [bounds]
command = "svgis draw floodviz/static/data/gages.json floodviz/static/data/cities.json -o " \
          "floodviz/static/data/sitemap.svg -f 500 -j epsg:2794 " \
          "-i \"name\" -c floodviz/static/css/site_style.css -b " + \
          str(bound1) + " " + str(bound2) + " " + str(bound3) + " " + str(bound4)
os.system(command)
