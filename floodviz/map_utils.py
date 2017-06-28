import requests
from flask import json


def site_dict(site_list, url_prefix):
    """Puts site data into a dictionary
    Args:
        site_list: A list of site ids to be queried on NWIS
        url_prefix: A string containing the beginning of the NWIS site url
    Returns:
        An array of dicts containing various site information in a usable format.
        If service call fails, function will return None
    """

    if not site_list:
        print("Site list empty, returning empty list")
        return []

    # generate the string of site ids for the url
    id_input_string = ",".join(site_list)

    # create the url
    url = url_prefix + "site/?format=rdb&sites=" + id_input_string + "&siteStatus=all"

    # get data from url
    req = requests.get(url)

    if req.status_code != 200:
        print("Error: service call failed")
        return

    if req.text == "":
        print("Service call returned no data")
        return []

    # data begins on first line that doesn't start with '#'
    data = req.text.splitlines()
    for line in req.text.splitlines():
        if line.startswith('#'):
            data.remove(line)
        else:
            break

    # make a list of dicts from data
    fields = data[0].split('\t')
    dnice = []
    for line in data[2:]:
        line = line.split('\t')
        line_dict = dict(zip(fields, line))
        dnice.append(line_dict)

    return dnice


def get_sites_geojson(data):
    """Writes site data to a .json file so it can be mapped
       Args:
           data: A list of dicts with data to be written to the file
        Returns:
            A string containing geojson data
    """

    geojson = "{ \"type\": \"FeatureCollection\", \"features\": [ \n"

    for i, datum in enumerate(data):
        geojson += "{ \"type\": \"Feature\",\n \"geometry\": {\n \"type\": \"Point\",\n \"coordinates\" : " \
                       "[" + datum.get('dec_long_va', 'n/a') + ", " + datum.get('dec_lat_va', 'n/a') \
                   + "]\n },\n \"properties\": {\n \"name\": \"" + datum.get('station_nm', 'n/a') \
                   + "\",\n \"id\": \"" + datum.get('site_no', 'n/a') + "\",\n \"huc\": \"" \
                   + datum.get('huc_cd', 'n/a') + "\" \n } \n }"
        # add a comma unless at end of list
        if data[i] != data[len(data) - 1]:
            geojson += ","
        geojson += "\n"
    geojson += " ] }"

    return geojson