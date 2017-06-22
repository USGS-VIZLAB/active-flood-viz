# below is for data processing #
import json
# # # # # # # # # # # # # # # # #
import requests
from flask import render_template

from . import app
from . import data_utils


@app.route('/home/')
def home():
    # new data store #
    newd = []
    sites = app.config['SITE_IDS']
    start_date = app.config['START_DT']
    end_date = app.config['END_DT']
    n_show_series = app.config['N_SERIES']
    hydro_meta = app.config['HYDRO_META']
    url_top = app.config['NWIS_SITE_SERVICE_ENDPOINT']
    sites_value_maxes = {}

    # Set up to retrieve all site ids from url? #
    for idx, site in enumerate(sites):
        url =  url_top +'iv/?site=' + site + '&startDT=' + \
              start_date + '&endDT=' + end_date + '&parameterCD=00060&format=json'

        r = requests.get(url)

        if r.status_code is 200:
            j = r.json()
            # custom data parsing utility. See data_utils.py
            data_utils.parse_hydrodata(j, newd, idx, sites_value_maxes)
    # custom filtering logic for hydrodata and hydrograph series. See data_utils.py
    data_utils.filter_hydrodata(newd, sites_value_maxes, n_show_series)
    

    # Save Data #
    with open('floodviz/static/data/hydrograph_data.json', 'w') as fout:  # Relative path so it's chill
        json.dump(newd, fout, indent=1)

    # For passing json as object to client javascript. (d3 needs a json file though)
    return render_template('index.html')
