import json

# open up and reference file and store the relevant data in a dictionary
def parse_reference_data(path):
    try:
        with open(path, 'r') as f:
            try:
                data = json.load(f)

            except json.decoder.JSONDecodeError:
                print('\n - File not valid json - \n')
                return None

    except FileNotFoundError:
        print('\n - File not found - \n')
        return None

    try:
        parsed_data = {}
        parsed_data['epsg'] = data['target_epsg'][5:]
        parsed_data['site_ids'] = data['site_ids']
        parsed_data['display_sites'] = data['display_sites']
        parsed_data['bbox'] = data['bbox']
        parsed_data['start_date'] = data['startDate']
        parsed_data['end_date'] = data['endDate']
        parsed_data['peak_dv_date'] = data['peak']['dv_date']
        parsed_data['peak_site'] = data['peak']['site']

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
        parsed_data['background_geojson_data'] = json.dumps({"type": "FeatureCollection", "features": background_geojson_data})

    except KeyError:
        print('\n - Missing data - \n')
        return None


    return parsed_data







