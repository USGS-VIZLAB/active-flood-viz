import requests

def req_peak_data(site, start_date, end_date, url_peak):
    """ 
    Requests water peak flow data in rdb format from NWIS water data
    service.  

    ARGS: 
        site - string site ID for the site to be charted
        start_date - starting date to chart peak flow data
        end_date - ending date to chart peak flow data
        url_peak - config varbile for nwis waterdata service endpoint url
    
    RETURNS:
        content - list of all lines in the data file 

    """
    url = url_peak + '?site_no=' + site + '&agency_cd=USGS&format=rdb'
    r = requests.get(url)
    content = r.text.splitlines()
    return content

def parse_peak_data(content, site_no):

    """ 
    Parses peak flow water data content and constructs a dictionary 
    appropriately formated for NVD3 charting library. 

    ARGS: 
        content - list of lines from peak flow data requested from NWIS waterdata service.
    
    RETURNS:
        peak_data - A dictonary reprsenting the peak flow data for a specific site 
    """
    peak_data = {'key': site_no, 'values': []}


    # TODO: duplicate data clean

    for line in content:
        if not line.startswith('USGS'):
            continue
        line = line.split('\t')
        year = line[2].split('-')[0]
        peak_val = int(line[4])
        peak_data['values'].append({'label': year, 'value': peak_val})

    return [peak_data]