from flask import render_template
import json
from . import app
from . import hydrograph_utils
from . import map_utils


@app.route('/home/')
def home():
    # new data store #
    sites = app.config['SITE_IDS']
    start_date = app.config['START_DT']
    end_date = app.config['END_DT']
    n_show_series = app.config['N_SERIES']
    hydro_meta = app.config['HYDRO_META']
    url_top = app.config['NWIS_SITE_SERVICE_ENDPOINT']

    j = hydrograph_utils.req_hydrodata(sites, start_date, end_date, url_top)
    all_series_data = hydrograph_utils.parse_hydrodata(j)

    with open('floodviz/static/data/hydrograph_data.json', 'w') as fout:
        json.dump(all_series_data, fout, indent=1)

    return render_template('index.html')


@app.route('/map/')
def sitemap():
    site_data = map_utils.site_dict(app.config['SITE_IDS'], app.config['NWIS_SITE_SERVICE_ENDPOINT'])
    site_data = map_utils.create_geojson(site_data)
    projection = map_utils.projection_info(app.config['PROJECTION_EPSG_CODE'], app.config['SPATIAL_REFERENCE_ENDPOINT'])

    # TODO: the following is a hack:
    with open('instance/counties.json', 'r') as bg_file:
        bg_data = json.load(bg_file)
    # End hack


    mapinfo = {
        'proj4string': projection,
        'width': 1000,
        'height': 600,
        'scale': .90,  # larger than .97 cuts off data
        'site_data': site_data,
        'bg_data': bg_data,
    }
    return render_template('sitemap.html', mapinfo=mapinfo)

