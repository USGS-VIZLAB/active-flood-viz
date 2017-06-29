import json
import xml.etree.ElementTree as ET
from string import Template

import requests


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


def alt_site_dict(ids, url_prefix):
    """
    Retrieves data on a list of sites and returns it in a list of dicts
    :param ids: list of site IDs
    :param url_prefix: NWIS site url prefix as a string
    :return: list of dictionaries describing the sites
    note that huc_cd, along with some other fields, will not be included
    """
    if not ids:
        print('No site IDs provided')
        return []

    # generate the string of site ids for the url
    id_input_string = ",".join(ids)
    url = url_prefix + "site/?format=mapper&sites=" + id_input_string + "&siteStatus=all"

    req = requests.get(url)
    if req.status_code != 200:
        print('request to NWIS has failed')
        return []

    sites = ET.fromstring(req.text).find('sites')
    # translate field names to match those returned in the original site_dict
    translation = {
        'sno': 'site_no',
        'sna': 'station_nm',
        'lat': 'dec_lat_va',
        'lng': 'dec_long_va'
    }
    site_list = []
    for site in sites.findall('site'):
        new_site = {}
        for k, v in translation.items():
            new_site[v] = site.get(k)
        # create_geojson expects this field
        new_site.update({'huc_cd': None})
        site_list.append(new_site)

    return site_list




