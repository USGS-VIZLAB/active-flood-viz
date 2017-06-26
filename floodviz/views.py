import json
import requests
from flask import render_template

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

    # Set up to retrieve all site ids from url #
    site_string = ''
    for idx, site in enumerate(sites):
        site = site +  ','
        site_string += site
        # Remove last comma
        if idx is len(sites) - 1:
            site_string = site_string[:-1]


    url =  url_top +'iv/?site=' + site_string + '&startDT=' + \
              start_date + '&endDT=' + end_date + '&parameterCD=00060&format=json'

    r = requests.get(url)

    if r.status_code is 200:
        j = r.json()['value']['timeSeries']
        # custom data parsing utility. See hydrograph_utils.py
        all_series_data = hydrograph_utils.parse_hydrodata(j)

    # Save Data #
    with open('floodviz/static/data/hydrograph_data.json', 'w') as fout:  # Relative path so it's chill
        json.dump(all_series_data, fout, indent=1)

    # For passing json as object to client javascript. (d3 needs a json file though)
    return render_template('index.html')
