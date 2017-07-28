import json

# open up and reference file and store the relevant data in a dictionary
def parse_reference_data(path):
    with open(path, 'r') as f:
        data = json.load(f)

        parsed_data = {}
        parsed_data['epsg'] = data['target_epsg'][5:]
        parsed_data['site_ids'] = data['site_ids']
        parsed_data['display_sites'] = data['display_sites']
        parsed_data['bbox'] = data['bbox']
        parsed_data['start_date'] = data['startDate']
        parsed_data['end_date'] = data['endDate']
        parsed_data['peak_dv_date'] = data['peak']['dv_date']
        parsed_data['peak_site'] = data['peak']['site']

        # grab the cities to be placed on the map
        city_geojson_data = []
        for i in range(0, len(data['reference']['features'])):
            if data['reference']['features'][i]['properties']['reftype'] == 'city':
                city_geojson_data.append(data['reference']['features'][i])
        parsed_data['city_geojson_data'] = {"type": "FeatureCollection", "features": city_geojson_data}

        # grab the rivers to be placed on the map
        river_geojson_data = []
        for i in range(0, len(data['reference']['features'])):
            if data['reference']['features'][i]['properties']['reftype'] == 'rivers':
                river_geojson_data.append(data['reference']['features'][i])
        parsed_data['river_geojson_data'] = json.dumps({"type": "FeatureCollection", "features": river_geojson_data})

        # grab the political/state borders to be placed on the map
        background_geojson_data = []
        for i in range(0, len(data['reference']['features'])):
            if data['reference']['features'][i]['properties']['reftype'] == 'politicalBoundaries':
                background_geojson_data.append(data['reference']['features'][i])
        parsed_data['background_geojson_data'] = json.dumps({"type": "FeatureCollection", "features": background_geojson_data})

        return parsed_data




