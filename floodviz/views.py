import json

from flask import render_template

from . import app
from . import hydrograph_utils


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
