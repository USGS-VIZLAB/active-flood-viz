import json

from flask import render_template, jsonify, url_for

from . import app
from . import hydrograph_utils
from . import map_utils
from . import peak_flow_utils
from . import REFERENCE_DATA as ref
from .linked_data_utils import LinkedData

url_nwis_prefix = app.config['NWIS_SITE_SERVICE_ENDPOINT']
linked_data = LinkedData()

thumbnail = app.config['THUMBNAIL']

@app.route('/')
def root():
    linked_data.set_dates(ref['start_date'], ref['end_date'])
    linked_data.set_location(ref['bbox'])
    linked_data.set_page_name(app.config['TITLE'])
    peakinfo = _peakflow_helper()
    mapinfo = _map_helper()
    display_sites = ref['display_sites']
    return render_template('index.html', mapinfo=mapinfo, peakinfo=peakinfo, display_sites=display_sites, linked_data=linked_data.assemble())


@app.route('/hydrograph/')
def hydrograph():
    display_sites = ref['display_sites']
    return render_template('hydrograph.html', display_sites=display_sites)


@app.route('/map/')
def sitemap():
    mapinfo = _map_helper()
    return render_template('map.html', mapinfo=mapinfo)

@app.route('/peakflow/')
def peakflow():
    peakinfo = _peakflow_helper()
    return render_template('peakflow.html', peakinfo=peakinfo)


@app.route('/timeseries.json')
def timeseries_data():
    hydro_start_date = ref['start_date']
    hydro_end_date = ref['end_date']
    sites = ref['site_ids']

    # Hydrodata data clean and write
    j = hydrograph_utils.req_hydrodata(sites, hydro_start_date, hydro_end_date, url_nwis_prefix)
    timeseries_data = hydrograph_utils.parse_hydrodata(j)

    if thumbnail:
        with open('floodviz/thumbnail/hydrograph_data.json', 'w') as f:
            k = hydrograph_utils.req_hydrodata(ref['display_sites'], hydro_start_date, hydro_end_date, url_nwis_prefix)
            thumbnail_data = hydrograph_utils.parse_hydrodata(k)
            json.dump(thumbnail_data, f)

    return jsonify(timeseries_data)


def _peakflow_helper():
    # Peak Flow config vars #
    peak_site = ref['peak_site']
    peak_end_date = ref['end_date']
    peak_dv_date = ref['peak_dv_date']
    url_peak_prefix = app.config['NWIS_PEAK_STREAMFLOW_SERVICE_ENDPOINT']

    historic_peaks = peak_flow_utils.req_peak_data(peak_site, peak_end_date, url_peak_prefix)
    daily_value_data = peak_flow_utils.req_peak_dv_data(peak_site, peak_dv_date, url_nwis_prefix)
    peak_data = peak_flow_utils.parse_peak_data(historic_peaks, daily_value_data)
    return peak_data


def _map_helper():
    site_data = map_utils.site_dict(ref['site_ids'], app.config['NWIS_SITE_SERVICE_ENDPOINT'])
    linked_data.set_gages(site_data)
    site_data = map_utils.create_geojson(site_data)
    projection = map_utils.projection_info(ref['epsg'], app.config['SPATIAL_REFERENCE_ENDPOINT'])
    bbox = ref['bbox']

    bg_data = json.loads(ref['background_geojson_data'])
    bg_data = map_utils.filter_background(bbox, bg_data)

    rivers = json.loads(ref['river_geojson_data'])

    ref_data = ref['city_geojson_data']

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
                        "coordinates": bbox[0:2]
                    },
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": bbox[2:4]
                    },
                }
            ]
        }
    })

    return mapinfo
