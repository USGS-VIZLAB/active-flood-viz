from string import Template
import requests

from . import utils


def site_dict(site_list, url_prefix):
    """
       Puts site data into a dictionary

       :param site_list: A list of site ids to be queried on NWIS
       :param url_prefix: A string containing the beginning of the NWIS site url

       :returns An array of dicts containing various site information in a usable format.
           If service call fails, function will return None
       """
    if not site_list:
        print('Site list empty, returning empty list')
        return []

        # generate the string of site ids for the url
    id_input_string = ','.join(site_list)

    # create the url
    url = url_prefix + 'site/'

    params = {
        'format': 'rdb',
        'sites': id_input_string,
        'siteStatus': 'all',
    }

    raw_gages = utils.parse_rdb(url, params)
    if raw_gages is not None:
        keep_fields = [
            'site_no',
            'station_nm',
            'dec_long_va',
            'dec_lat_va',
            'huc_cd'
        ]
        gages = []
        for raw in raw_gages:
            gage = {k: raw[k] for k in keep_fields}
            gages.append(gage)
    else:
        print('utils rdb_parser has returned no data to map utils')
        gages = None

    return gages


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


def filter_background(bbox, bg_data):
    """
    Takes bounding box and background geojson file assumed to be the US states, and outputs a geojson-like dictionary
    containing only those features with at least one point within the bounding box, or any state that completely
    contains the bounding box.

    This tests if a feature contains the bounding box by drawing the box that contains the feature and checking if that
    box also contains the bounding box. Because features are odd shapes, this may find that more than one feature
    completely contains the bounding box. E.g., if you draw a box around Maryland it will also contain a chunk of West
    Virginia. To deal with this, we are allowed to find that multiple states contain the bounding box.

    :param bbox: The coordinates of the bounding box as [lon, lat, lon, lat]
    :param bg_data: a geojson-like dict describing the background
    :return: the features from bg_filename whose borders intersect bbox OR the feature which completely contains bbox
    """
    box_lon = [bbox[0], bbox[2]]
    box_lat = [bbox[1], bbox[3]]

    features = bg_data['features']
    in_box = []
    for f in features:
        starting_len = len(in_box)

        # Define points for bounding box around the feature.
        feature_max_lat = -90
        feature_max_lon = -180
        feature_min_lat = 90
        feature_min_lon = 180

        coordinates = f['geometry']['coordinates']

        for group in coordinates:
            if len(in_box) > starting_len:
                # This feature has already been added
                break
            # actual points for MultiPolygons are nested one layer deeper than those for polygons
            if f['geometry']['type'] == 'MultiPolygon':
                geom = group[0]

            else:
                geom = group

            for lon, lat in geom:
                # check if any point along the state's borders falls within the bounding box.
                if min(box_lon) <= lon <= max(box_lon) and min(box_lat) <= lat <= max(box_lat):
                    in_box.append(f)
                    break

                # If any point of a feature falls within the bounding box, then the feature cannot contain the box,
                #  so this only needs to be run if the above if statement is not executed
                feature_min_lon = min(feature_min_lon, lon)
                feature_min_lat = min(feature_min_lat, lat)
                feature_max_lon = max(feature_max_lon, lon)
                feature_max_lat = max(feature_max_lat, lat)

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
