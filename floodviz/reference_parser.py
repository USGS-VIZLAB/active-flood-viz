import json

# open up and reference file and store the relevant data in variables
with open('floodviz/static/reference/reference.json', 'r') as f:
    data = json.load(f)

    epsg = data['target_epsg'][5:]
    site_ids = data['site_ids']
    display_sites = data['display_sites']
    bbox = data['bbox']
    start_date = data['startDate']
    end_date = data['endDate']
    peak_dv_date = data['endDate']
    peak_site = data['peak']['site']

    # grab the cities to be placed on the map
    city_data = []
    for i in range(0, len(data['reference']['features'])):
        if data['reference']['features'][i]['properties']['reftype'] == 'city':
            city_data.append(data['reference']['features'][i])
    city_data = {"type": "FeatureCollection", "features": city_data}

    # grab the rivers to be placed on the map
    river_data = []
    for i in range(0, len(data['reference']['features'])):
        if data['reference']['features'][i]['properties']['reftype'] == 'rivers':
            river_data.append(data['reference']['features'][i])
    river_data = json.dumps({"type": "FeatureCollection", "features": river_data})

    # grab the political/state borders to be placed on the map
    background_data = []
    for i in range(0, len(data['reference']['features'])):
        if data['reference']['features'][i]['properties']['reftype'] == 'politicalBoundaries':
            background_data.append(data['reference']['features'][i])
    background_data = json.dumps({"type": "FeatureCollection", "features": background_data})




