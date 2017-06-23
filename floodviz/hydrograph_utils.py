from datetime import datetime
import operator
import time


def parse_hydrodata(jdata):
    siteName = jdata['sourceInfo']['siteName']
    key = siteName  # Key for this series
    tempd = {'key': key, 'values': [], 'max_val': 0}

    # Fill new data for this series
    max_val = 0
    for idx2, obj in enumerate(jdata['values'][0]['value']):
        value = obj['value']
        # For filtering series #
        if max_val < float(value):
            tempd['max_val'] = float(value)

        dt = obj['dateTime']
        date = dt.split('T')[0]
        t = dt.split('T')[1].split('.')[0]
        # reformat datetime for python datetime #   
        dt = datetime.strptime(date + ' ' + t, '%Y-%m-%d %H:%M:%S')
        # Convert to milliseconds for use with d3 x axis format
        dt_ms = time.mktime(dt.timetuple()) * 1000
        # (for below if statment) create dummy value for nvd3 issue at https://github.com/novus/nvd3/issues/695 #
        if idx2 is 0: # First datapoint of this site
            tempd['values'].append({'date': date, "time": 0, "time_mili": dt_ms, 'value': 0})
   
        tempd['values'].append({'date': date, "time": t, "time_mili": dt_ms, 'value': value})

    return tempd


    
def filter_hydrodata(tempd, sites_value_maxes, n_show_series):
    # Filter out the sites to plot
    sorted_avg = sorted(sites_value_maxes.items(), key=operator.itemgetter(1), reverse=True)
    rm = sorted_avg[n_show_series:]  # remove all but top x series
    rm = dict(rm)
    ret = []
    for item in tempd:
        siteN = item['key']
        if rm.get(siteN) is None:
            ret.append(item)
    return ret
