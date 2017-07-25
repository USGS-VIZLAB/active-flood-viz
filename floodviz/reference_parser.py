import json

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
    city_data = []
    for i in range(0, len(data['reference']['features'])):
        if data['reference']['features'][i]['properties']['reftype'] == 'city':
            city_data.append(data['reference']['features'][i])

    city_data = {"type": "FeatureCollection", "features": city_data}

    river_data = []
    for i in range(0, len(data['reference']['features'])):
        if data['reference']['features'][i]['properties']['reftype'] == 'rivers':
            river_data.append(data['reference']['features'][i])

    river_data = json.dumps({"type": "FeatureCollection", "features": river_data})

    background_data = []
    for i in range(0, len(data['reference']['features'])):
        if data['reference']['features'][i]['properties']['reftype'] == 'politicalBoundaries':
            background_data.append(data['reference']['features'][i])

    background_data = json.dumps({"type": "FeatureCollection", "features": background_data})




