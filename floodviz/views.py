import json
from flask import render_template

from . import app
from . import hydrograph_utils
from . import map_utils
from . import peak_flow_utils


@app.route('/home/')
def home():
    # Hydrograph config vars #
    sites = app.config['SITE_IDS']
    hydro_start_date = app.config['H_START_DT']
    hydro_end_date = app.config['H_END_DT']
    hydro_meta = app.config['HYDRO_META']
    url_hydro = app.config['NWIS_SITE_SERVICE_ENDPOINT']
    # Peak Flow config vars #
    peak_site = app.config['PEAK_SITE']
    peak_start_date = app.config['P_START_DT']
    peak_end_date = app.config['P_END_DT']
    url_peak = app.config['NWIS_WATERPEAK_SITE_SERVICE_ENDPOINT']

    # Hydrodata data clean and write
    j = hydrograph_utils.req_hydrodata(sites, hydro_start_date, hydro_end_date, url_hydro)
    all_series_data = hydrograph_utils.parse_hydrodata(j)
    with open('floodviz/static/data/hydrograph_data.json', 'w') as fout: 
        json.dump(all_series_data, fout, indent=1)

    # Peak Water Flow data clean and write 
    content = peak_flow_utils.req_peak_data(peak_site, peak_start_date, peak_end_date, url_peak)
    peak_data = peak_flow_utils.parse_peak_data(content, peak_site)
    with open('floodviz/static/data/peak_flow_data.json', 'w') as fout: 
        json.dump(peak_data, fout, indent=1)


    return render_template('index.html')
