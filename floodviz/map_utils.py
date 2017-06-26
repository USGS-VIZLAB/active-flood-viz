import requests
import json
from string import Template

def site_dict(site_list, url_prefix):
    """Puts site data into a dictionary

    Args:
        site_list: A list of site ids to be queried on NWIS
        url_prefix: The beginning of the NWIS url

    Returns:
        A dict containing various site information in a usable format.
    """

    # generate the string of site ids for the url
    id_input_string = ",".join(site_list)

    # create the url
    url = url_prefix + "/?format=rdb&sites=" + id_input_string + "&siteStatus=all"

    # get data from url
    req = requests.get(url)

    # put data into list
    data = req.text.splitlines()[29:]

    # make a list of dicts from data
    fields = data[0].split('\t')
    dnice = []
    for line in data[2:]:
        line = line.split('\t')
        line_dict = dict(zip(fields, line))
        dnice.append(line_dict)

    return dnice


def write_geojson(filename, data):
    """Writes site data to a .json file so it can be mapped

       Args:
           filename: the file to be written to
           data: the data to be written to the file
    """
    data = create_geojson(data)
    with open(filename, "w+") as f:
        json.dump(data, f, indent=True)


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
        this should found under SPATIAL_REFERENCE_ENDPOINT in `config.py`

    :return: the proj4 projection definition string of the desired projection
    """
    url = Template(url)
    url = url.substitute(epsg_code=str(code))
    req = requests.get(url)
    return req.text