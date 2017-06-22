from flask import request, render_template, abort

# below is for data processing #
import json
import time
from datetime import datetime
import requests
import operator
# # # # # # # # # # # # # # # # # #

from . import app


@app.route('/home/')
def home():
    # new data store #
    newd = []
    sites_value_maxs = {}
    sites = app.config['SITE_IDS']
    start_date = app.config['START_DT']
    end_date = app.config['END_DT']
    n_show_series = app.config['N_SERIES']
    hydro_meta = app.config['HYDRO_META']

    # Set up to retrieve all site ids from url? #
    for idx, site in enumerate(sites):
        url = 'https://nwis.waterservices.usgs.gov/nwis/iv/?site=' + site + '&startDT=' + \
              start_date + '&endDT=' + end_date + '&parameterCD=00060&format=json'

        try:
            r = requests.get(url)
        except ():
            print('Unable to retrieve URL: ' + url)
            continue

        if r.status_code is 200:
            j = r.json()
            site_name = j['value']['timeSeries'][0]['sourceInfo']['site_name']
            key = site_name  # Key for this series
            newd.append({'key': key, 'values': [], 'max': 0})
            # Fill new data
            max_val = 0
            for idx2, obj in enumerate(j['value']['timeSeries'][0]['values'][0]['value']):
                value = obj['value']
                # For filtering series #
                if max_val < float(value):
                    max_val = float(value)

                dt = obj['dateTime']
                date = dt.split('T')[0]
                t = dt.split('T')[1].split('.')[0]
                # reformat datetime for python datetime #
                dt = datetime.strptime(date + ' ' + t, '%Y-%m-%d %H:%M:%S')
                # Convert to milliseconds for use with d3 x axis format
                dt_ms = time.mktime(dt.timetuple()) * 1000
                # create dummy value for nvd3 issue at https://github.com/novus/nvd3/issues/695 #
                if idx2 is 0:
                    newd[idx]['values'].append(
                        {'date': start_date, "time": 0, "time_mili": dt_ms, 'value': 0, 'max': max_val})
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                newd[idx]['values'].append(
                    {'date': date, "time": t, "time_mili": dt_ms, 'value': value, 'max': max_val})

            sites_value_maxs[key] = max_val

    # Filter out the sites to plot # TODO: I can make this faster with one pass HASH
    sorted_avg = sorted(sites_value_maxs.items(), key=operator.itemgetter(1), reverse=True)
    remove = sorted_avg[n_show_series:]  # remove all but top x series
    for item in remove:
        key = item[0]
        for site in newd:
            if key is site['key']:
                newd.remove(site)

    # Save Data #
    with open('floodviz/static/data/hydrograph_data.json', 'w') as fout:  # Relative path so it's chill
        json.dump(newd, fout, indent=1)

    # For passing json as object to client javascript. (d3 needs a json file though)
    return render_template('index.html', hydrometa=json.dumps(hydro_meta))
