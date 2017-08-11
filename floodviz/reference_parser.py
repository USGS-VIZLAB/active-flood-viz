import json


def parse_reference_data(path):
    """
    open up and reference file and store the relevant data in a dictionary
    :param: path Path to reference file
    :return: Dictionary containing data parsed from reference file.
    """
    try:
        with open(path, 'r') as f:
            try:
                data = json.load(f)

            except json.decoder.JSONDecodeError:
                print('\n - Reference file is not valid json - \n')
                return None

    except FileNotFoundError as e:
        print(e)
        print('\n -  Reference file not found - \n')
        return None

    try:
        parsed_data = {
            'epsg': data['target_epsg'][5:],
            'site_ids': data['site_ids'],
            'display_sites': data['display_sites'],
            'bbox': data['bbox'],
            'start_date': data['startDate'],
            'end_date': data['endDate'],
            'peak_dv_date': data['peak']['dv_date'],
            'peak_site': data['peak']['site']
        }

        features = data['reference']['features']

        # grab the cities to be placed on the map
        city_geojson_data = [features[i] for i in range(0, len(features))
                             if features[i]['properties']['reftype'] == 'city']
        parsed_data['city_geojson_data'] = {"type": "FeatureCollection", "features": city_geojson_data}

        # grab the rivers to be placed on the map
        river_geojson_data = [features[i] for i in range(0, len(features))
                              if features[i]['properties']['reftype'] == 'rivers']
        parsed_data['river_geojson_data'] = json.dumps({"type": "FeatureCollection", "features": river_geojson_data})

        # grab the political/state borders to be placed on the map
        background_geojson_data = [features[i] for i in range(0, len(features))
                                   if features[i]['properties']['reftype'] == 'politicalBoundaries']
        parsed_data['background_geojson_data'] = json.dumps(
            {"type": "FeatureCollection", "features": background_geojson_data})

    except KeyError:
        print('\n - Missing data during reference parsing - \n')
        return None

    return parsed_data
