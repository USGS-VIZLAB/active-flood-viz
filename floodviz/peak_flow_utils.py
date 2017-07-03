import requests

def req_peak_data(site, start_date, end_date, url_pefix):
    """ 
    This function first requests water peak flow data in
    rdb format from NWIS peak water data service.

    ARGS: 
        site - string site ID for the site to be charted
        start_date - starting date to chart peak flow data
        end_date - ending date to chart peak flow data
        url_pefix - config varbile for nwis peak waterdata service endpoint url
    
    RETURNS:
        content - list of all lines in the data file 

    """
    # peak value historical data #
    content = []
    url = url_pefix + '?site_no=' + site + '&agency_cd=USGS&format=rdb' + '&end_date=' + end_date
    r = requests.get(url)
    if r.status_code is 200:
        content = r.text.splitlines()
    return content

def req_peak_dv_data(site, date, url_prefix):
    """ 
    requests data from the Daily Value NWIS water data service
    for creating the lollipop svg elements for the current year.

    ARGS: 
        site - string site ID for the site to be charted
        date - date to chart lollipop flow data
        url_pefix - config varbile for nwis peak waterdata service endpoint url
    
    RETURNS:
        content - list of all lines in the data file 

    """
    content = []
    url = url_prefix + 'dv/?format=rdb&sites=' + site + '&startDT=' + date + '&endDT=' + date + '&siteStatus=all'
    r = requests.get(url)
    if r.status_code is 200:
        content = r.text.splitlines()
    return content



def parse_peak_data(peak_data, dv_data, site_no):

    """ 
    Parses peak flow water data peak_data and constructs a dictionary 
    appropriately formated for D3 charting library. 

    ARGS: 
        peak_data - list of lines from peak flow data requested from NWIS waterdata service.
    
    RETURNS:
        peak_data - A list holding the peak flow data points
        (each as a dict) for a specific site 
    """
    
    all_data = []
    seen = set([])
    # parse peak_data 
    for line in peak_data:
        if not line.startswith('USGS'):
            continue
        line = line.split('\t')
        year = line[2].split('-')[0]
        # remove duplicate years
        if year in seen:
            continue
        else:
            seen.add(year)
        if line[4]:
            peak_val = int(line[4])
            all_data.append({'label': year, 'value': peak_val})
    # parse daily_value data
    for line in dv_data:
        if not line.startswith('USGS'):
            continue
        line = line.split('\t')
        year = line[2].split('-')[0]
        # below conditon will favor the peak value retrieved from
        # peak value data opposed to daily value data if peak value data is available
        if year in seen:
            break
        if line[3]:
            peak_val = float(line[3])
            all_data.append({'label': year, 'value': peak_val})

    return all_data