import json

from flask import render_template, jsonify, url_for

from . import app
from . import hydrograph_utils
from . import map_utils
from . import peak_flow_utils

url_nwis_prefix = app.config['NWIS_SITE_SERVICE_ENDPOINT']


@app.route('/')
def root():
    peakinfo = _peakflow_helper()
    mapinfo = _map_helper()
    return render_template('index.html', mapinfo=mapinfo, peakinfo=peakinfo)

@app.route('/hydrograph/')
def hydrograph():
    return render_template('hydrograph.html')

@app.route('/map/')
def sitemap():
    mapinfo = _map_helper()
    return render_template('map.html', mapinfo=mapinfo)

@app.route('/timeseries/')
def timeseries_data():
    hydro_start_date = app.config['EVENT_START_DT']
    hydro_end_date = app.config['EVENT_END_DT']
    sites = app.config['SITE_IDS']

    # Hydrodata data clean and write
    j = hydrograph_utils.req_hydrodata(sites, hydro_start_date, hydro_end_date, url_nwis_prefix)
    timeseries_data = hydrograph_utils.parse_hydrodata(j)
    return jsonify(timeseries_data)


def _peakflow_helper():
    # Peak Flow config vars #
    peak_site = app.config['PEAK_SITE']
    peak_start_date = app.config['EVENT_START_DT']
    peak_end_date = app.config['EVENT_END_DT']
    peak_dv_date = app.config['PEAK_DV_DT']
    url_peak_prefix = app.config['NWIS_PEAK_STREAMFLOW_SERVICE_ENDPOINT']

    # Peak Water Flow data clean and write 
    content = peak_flow_utils.req_peak_data(peak_site, peak_start_date, peak_end_date, url_peak_prefix)
    daily_value_data = peak_flow_utils.req_peak_dv_data(peak_site, peak_dv_date, url_nwis_prefix)
    peak_data = peak_flow_utils.parse_peak_data(content, daily_value_data)
    return peak_data

def _map_helper():
    site_data = map_utils.site_dict(app.config['SITE_IDS'], app.config['NWIS_SITE_SERVICE_ENDPOINT'])
    site_data = map_utils.create_geojson(site_data)
    projection = map_utils.projection_info(app.config['PROJECTION_EPSG_CODE'], app.config['SPATIAL_REFERENCE_ENDPOINT'])
    
    with open(app.config['BACKGROUND_FILE'], 'r') as bg_file:
        bg_data = json.load(bg_file)
    bg_data = map_utils.filter_background(app.config['BOUNDING_BOX'], bg_data)

    with open(app.config['RIVERS_FILE'], 'r') as rivers_file:
        rivers = json.load(rivers_file)

    ref_data = app.config['REFERENCE_DATA']


    mapinfo = app.config['MAP_CONFIG']
    mapinfo.update({
        'proj4string': projection,
        'site_data': site_data,
        'bg_data': bg_data,
        'ref_data': ref_data,
        'rivers_data': rivers,
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
