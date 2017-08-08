from datetime import datetime
import time
import requests

def parse_hydrodata(jdata):
    
    """ 
    Parses json Hydrodata from NWIS webservice
    and formats for D3 charting library. Upon failure, this will
    return empty data list.

    ARGS: 
        jdata (list of one dictonary) - json object in a list which contains 
        time series data for all sites listed in config.py SITE_IDs.
    
    RETURNS:
        All series data correctly formated for D3.
        This is also a list of python dictonaries.

    """
    all_series_data = []
    
    if jdata is not None:
        for site in jdata:

            site_name = site['sourceInfo']['siteName']
            site_id = site['sourceInfo']['siteCode'][0]['value']
            timezone = site['sourceInfo']['timeZoneInfo']['defaultTimeZone']['zoneAbbreviation']

            # Fill data for this series
            for obj in site['values'][0]['value']:
                value = obj['value']
                dt = obj['dateTime']
                date = dt.split('T')[0]
                t = dt.split('T')[1].split('.')[0]
                # reformat datetime for python datetime #
                dt = datetime.strptime(date + ' ' + t, '%Y-%m-%d %H:%M:%S')
                # Convert to milliseconds for use with d3 x axis format
                dt_ms = time.mktime(dt.timetuple()) * 1000
                all_series_data.append({'key': site_id, 'name': site_name, 'date': date, "time": t,
                                        'timezone': timezone, "time_mili": dt_ms, 'value': value})

    return all_series_data


def req_hydrodata(sites, start_date, end_date, url_top):

    """ 
    Requests hydrodata from nwis web service based on passed in parameters.
    Upon request failure, this will return None. 

    ARGS: 
        sites - List of site IDs to request
        start_date - start date for the time series data
        end_date - end date for the time series data
        url_top - URL endpoint for the nwis web service
    
    RETURNS:
        returns a list of one dictonary with the requested data for
        all series from the nwis service
    
    """
    ret = None
    if len(sites) is not 0 and start_date and end_date and url_top:
        # Form URL
        sites = [str(site) for site in sites]
        sites_string = ','.join(sites)
        url =  url_top +'iv/?site=' + sites_string + '&startDT=' + \
              start_date + '&endDT=' + end_date + '&parameterCD=00060&format=json'

        try:
            r = requests.get(url)
            if r.status_code is 200:
                ret = r.json()['value']['timeSeries']
            else:
                print('\n - Bad Request -\n')

        except requests.exceptions.RequestException as e:
            print('\n - Malformed URL - \n')

    else:
        print('\nConfig Varibles Empty\n')
    
    return ret
