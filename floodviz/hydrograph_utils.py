from datetime import datetime
import time
import requests


def parse_hydrodata(jdata):
    
    """ 
    Parses json Hydrodata from NWIS webservice
    and formats for NVD3 charting library.

    ARGS: 
        jdata (list of dictonaries) - json objects in a list which contains 
        time series data for all sites listed in config.py SITE_IDs.
    
    RETURNS:
        All series data correctly formated for NVD3 charting library. 
        This is also a list of python dictonaries where each dictionary 
        corresponds to a different site.   

    """

    all_series_data = []

    for idx, site in enumerate(jdata):
        site_name = site['sourceInfo']['siteName']
        all_series_data.append({'key': site_name, 'values': [], 'max_val': 0})

        # Fill new data for this series
        for idx2, obj in enumerate(site['values'][0]['value']):
            value = obj['value']
            dt = obj['dateTime']
            date = dt.split('T')[0]
            t = dt.split('T')[1].split('.')[0]
            # reformat datetime for python datetime #   
            dt = datetime.strptime(date + ' ' + t, '%Y-%m-%d %H:%M:%S')
            # Convert to milliseconds for use with d3 x axis format
            dt_ms = time.mktime(dt.timetuple()) * 1000
            # (for below if statment) create dummy value for nvd3 issue at https://github.com/novus/nvd3/issues/695 #
            if idx2 is 0: # First datapoint of this site
                all_series_data[idx]['values'].append({'date': date, "time": 0, "time_mili": dt_ms, 'value': 0})

            all_series_data[idx]['values'].append({'date': date, "time": t, "time_mili": dt_ms, 'value': value})

    return all_series_data


def req_hydrodata(sites, start_date, end_date, url_top):

    """ 
    Requests hydrodata from nwis web service based on passed in parameters. 

    ARGS: 
        sites - List of site IDs to request
        start_date - start date for the time series data
        end_date - end date for the time series data
        url_top - URL endpoint for the nwis web service
    
    RETURNS:
        returns a dictonary with the requested data from the nwis service 
    
    """


    # Set up to retrieve all site ids for hydrograph from url #
    sites_string = ','.join(sites)
    url =  url_top +'iv/?site=' + sites_string + '&startDT=' + \
              start_date + '&endDT=' + end_date + '&parameterCD=00060&format=json'
    r = requests.get(url)
    if r.status_code is 200:
        return r.json()['value']['timeSeries']
