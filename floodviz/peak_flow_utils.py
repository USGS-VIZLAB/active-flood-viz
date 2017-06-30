import requests

def req_peak_data(site, start_date, end_date, url_peak):
    """ 
    This function first requests water peak flow data in
    rdb format from NWIS peak water data service. Then it
    requests data from the Daily Value NWIS water data service
    for creating the lollipop svg elements for the current year.

    ARGS: 
        site - string site ID for the site to be charted
        start_date - starting date to chart peak flow data
        end_date - ending date to chart peak flow data
        url_peak - config varbile for nwis peak waterdata service endpoint url
    
    RETURNS:
        content - list of all lines in the data file 

    """
    # peak value historical data #
    content = []
    url = url_peak + '?site_no=' + site + '&agency_cd=USGS&format=rdb'
    r = requests.get(url)
    if r.status_code is 200:
        content = r.text.splitlines()
    
        # TODO: retrive DV data -- from : https://waterservices.usgs.gov/nwis/dv/?sites=05411850&startDT=2008-05-20&endDT=2008-07-05&siteStatus=all&format=json


    return content

def parse_peak_data(content, site_no):

    """ 
    Parses peak flow water data content and constructs a dictionary 
    appropriately formated for D3 charting library. 

    ARGS: 
        content - list of lines from peak flow data requested from NWIS waterdata service.
    
    RETURNS:
        peak_data - A list holding the peak flow data points
        (each as a dict) for a specific site 
    """
    
    peak_data = []
    seen = set([])
    # TODO: duplicate data clean
    for line in content:
        if not line.startswith('USGS'):
            continue
        line = line.split('\t')
        year = line[2].split('-')[0]
        # remove duplicate years
        if year in seen:
            continue
        else:
            seen.add(year)
        peak_val = int(line[4])
        peak_data.append({'label': year, 'value': peak_val})
    return peak_data