import json
import xml.etree.ElementTree as ET
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
        return None

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

    keep_fields = [
        'site_no',
        'station_nm',
        'dec_long_va',
        'dec_lat_va',
        'huc_cd'
    ]

    # make a list of dicts from data, remove any aberrant spaces
    fields = [field.strip() for field in data[0].split('\t')]
    dnice = []
    for line in data[2:]:
        line = [item.strip() for item in line.split('\t')]
        line_dict = dict(zip(fields, line))
        try:
            filtered_line_dict = {k: line_dict[k] for k in keep_fields}
        except KeyError:
            raise KeyError
        dnice.append(filtered_line_dict)

    return dnice


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


def filter_background(bbox, bg_filename):
    """
    Takes bounding box and background geojson file assumed to be the US states, and outputs a geojson-like dictionary
    containing only those features (states) whose borders at some point intersect the bounding box, OR the state that
    completely contains the bounding box.

    :param bbox: The coordinates of the bounding box
    :param bg_filename: the name of the background file
    :return: the features from bg_filename whose borders intersect bbox OR the feature which completely contains bbox
    """
    box_lon = [bbox[0], bbox[2]]
    box_lat = [bbox[1], bbox[3]]
    with open(bg_filename, 'r') as bg_file:
        bg = json.load(bg_file)
    features = bg['features']
    in_box = []
    for f in features:
        starting_len = len(in_box)

        # Define points for bounding box around the state.
        feature_max_lat = float('-inf')
        feature_max_lon = float('-inf')
        feature_min_lat = float('inf')
        feature_min_lon = float('inf')
        
        coordinates = f['geometry']['coordinates']

        for group in coordinates:
            if len(in_box) > starting_len:
                # This feature has already been added
                break
            # actual points for MultiPolygons are nested one layer deeper than those for polygons
            if f['geometry']['type'] == 'MultiPolygon':
                group = group[0]

            for pair in group:
                # check if any point along the state's borders falls within the bounding box.
                if min(box_lon) <= pair[0] <= max(box_lon) and min(box_lat) <= pair[1] <= max(box_lat):
                    in_box.append(f)
                    break

                # We only need to check the box around the state if we don't add the state based on an intersection.
                feature_min_lon = min(feature_min_lon, pair[0])
                feature_min_lat = min(feature_min_lat, pair[1])
                feature_max_lon = max(feature_max_lon, pair[0])
                feature_max_lat = max(feature_max_lat, pair[1])

        # If the box containing a feature also contains the bounding box, keep this feature
        # Allow adding more than one because otherwise MD contains boxes in WV, and CA would contain most of NV.
        if feature_min_lat < min(box_lat) and feature_max_lat > max(box_lat) and \
                feature_min_lon < min(box_lon) and feature_max_lon > max(box_lon):
            in_box.append(f)

    keepers = {
        'type': 'FeatureCollection',
        'features': in_box
    }

    return keepers
