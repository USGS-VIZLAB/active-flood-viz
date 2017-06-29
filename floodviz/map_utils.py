import json
from string import Template

import requests


def site_dict(site_list, url_prefix):
    """
    Puts site data into a dictionary

    :param site_list: A list of site ids to be queried on NWIS
    :param url_prefix: A string containing the beginning of the NWIS site url

    :returns An array of dicts containing various site information in a usable format.
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


def write_geojson(filename, data):
    """
    Writes site data to a .json file so it can be mapped
    This version will create the file if it does not exist and overwrite it if it does. You have been warned.

    :param  filename: the file to be written to
    :param  data: the data to be written to the file
    """
    data = create_geojson(data)
    with open(filename, "w+") as file:
        json.dump(data, file, indent=True)


def create_geojson(data):
    """
    :param data: a dictionary of sites to be transformed into geojson
    :return: a geojson string representing the sites
    """

    new_data = {
        "type": "FeatureCollection",
        "features": []
    }
    for original in data:
        item = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    original['dec_long_va'],
                    original['dec_lat_va']
                ]
            },
            'properties': {
                'name': original['station_nm'],
                'id': original['site_no'],
                'huc': original['huc_cd']
            }
        }
        new_data['features'].append(item)
    return new_data


def projection_info(code, url):
    """
    :param code: the EPSG code of the projection we wish to use

    :param url: A python string TEMPLATE in which ${epsg_code} will be replaced with `code`
        A valid example is SPATIAL_REFERENCE_ENDPOINT in `config.py`

    :return: the proj4 projection definition string of the desired projection, or None if no such projection is found
    """
    url = Template(url)
    url = url.substitute(epsg_code=str(code))
    req = requests.get(url)
    if req.status_code != 200:
        return None
    return req.text
