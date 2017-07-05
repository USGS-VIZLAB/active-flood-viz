import json

from flask import render_template

from . import app
from . import hydrograph_utils
from . import map_utils


@app.route('/')
def root():
    _hydrograph_helper()
    mapinfo = _map_helper()
    return render_template('index.html', mapinfo=mapinfo)


@app.route('/hydrograph/')
def home():
    _hydrograph_helper()
    return render_template('hydrograph.html')


@app.route('/map/')
def sitemap():
    mapinfo = _map_helper()
    return render_template('sitemap.html', mapinfo=mapinfo)


def _hydrograph_helper():
    # new data store #
    sites = app.config['SITE_IDS']
    start_date = app.config['H_START_DT']
    end_date = app.config['H_END_DT']
    hydro_meta = app.config['HYDRO_META']
    url_top = app.config['NWIS_SITE_SERVICE_ENDPOINT']

    j = hydrograph_utils.req_hydrodata(sites, start_date, end_date, url_top)
    all_series_data = hydrograph_utils.parse_hydrodata(j)

    with open('floodviz/static/data/hydrograph_data.json', 'w') as fout:
        json.dump(all_series_data, fout, indent=1)


def _map_helper():
    site_data = map_utils.site_dict(app.config['SITE_IDS'], app.config['NWIS_SITE_SERVICE_ENDPOINT'])
    site_data = map_utils.create_geojson(site_data)
    projection = map_utils.projection_info(app.config['PROJECTION_EPSG_CODE'], app.config['SPATIAL_REFERENCE_ENDPOINT'])

    with open(app.config['BACKGROUND_FILE'], 'r') as bg_file:
        bg_data = json.load(bg_file)
    bg_data = map_utils.filter_background(app.config['BOUNDING_BOX'], bg_data)

    ref_data = app.config['REFERENCE_DATA']

    mapinfo = app.config['MAP_CONFIG']
    mapinfo.update({
        'proj4string': projection,
        'site_data': site_data,
        'bg_data': bg_data,
        'ref_data': ref_data,
        # add bounding box as geojson
        'bounds': {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": app.config['BOUNDING_BOX'][0:2]
                    },
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": app.config['BOUNDING_BOX'][2:4]
                    },
                }
            ]
        }
    })
    return mapinfo
