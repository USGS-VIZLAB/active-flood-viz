from datetime import datetime
import operator
import time


def parse_hydrodata(jdata, newd, idx, sites_value_maxes):
    siteName = jdata['value']['timeSeries'][0]['sourceInfo']['siteName']
    key = siteName  # Key for this series
    newd.append({'key': key, 'values': [], 'max': 0})
    # Fill new data
    max_val = 0
    for idx2, obj in enumerate(jdata['value']['timeSeries'][0]['values'][0]['value']):
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
        # (for below if statment) create dummy value for nvd3 issue at https://github.com/novus/nvd3/issues/695 #
        if idx2 is 0: # First datapoint of this site
            newd[idx]['values'].append({'date': date, "time": 0, "time_mili": dt_ms, 'value': 0, 'max': max_val})
   
        newd[idx]['values'].append({'date': date, "time": t, "time_mili": dt_ms, 'value': value, 'max': max_val})

    sites_value_maxes[key] = max_val

    
def filter_hydrodata(newd, sites_value_maxes, n_show_series):
    # Filter out the sites to plot # TODO: I can make this faster with one pass HASH
    sorted_avg = sorted(sites_value_maxes.items(), key=operator.itemgetter(1), reverse=True)
    remove = sorted_avg[n_show_series:]  # remove all but top x series
    for item in remove:
        key = item[0]
        for site in newd:
            if key is site['key']:
                newd.remove(site)