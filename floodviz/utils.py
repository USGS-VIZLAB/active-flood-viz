import requests

"""
    Takes a valid url and a dictionary of expected column header strings as keys (values do not matter).
    parse_rdb then requests data from the service at url, and extracts data matching any header values.
     
    Data is returned as a list of dict objects, where each object represents a data point. 

"""


def parse_rdb(url, header_values):
    content = None
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print('- Bad URL -')
    else:
        if r.status_code is 200:
            content = r.text.splitlines()
    if content:
        all_data = []
        keep_headers = {}
        found_headers = False
        for line in content:
            if line.startswith('#'):
                continue
            # should run once. Used to map column headers to line split indices.
            if not found_headers:
                raw_headers = line.split('\t')
                for idx, key in enumerate(raw_headers):
                    if header_values.get(key) is not None:
                        keep_headers[key] = idx
                found_headers = True
                continue
            else:
                if line.startswith('USGS'):
                    line = line.split('\t')
                    data_point = {}
                    for key, value in keep_headers.items():
                        data_point[key] = line[value]
                    all_data.append(data_point)
        content = all_data
    return content

""" 
    Takes a web service endpoint, a dictionary of key/value pairs for the query parameters
    and returns the formatted url. 

    ARGS: 
        endpoint - String specifiying the web service url
        params - dictionary holding url parameters
            
            possible keys:
                'sites' (mandatory) - List of string site_ids
                'site_query' (mandatory) - service specific string for url construction that targets the sites.
                'format' (mandatory) - service specific string for format of the data returned from service
                'extra' - service specific string prepended to the format if needed.
                'start_date_query' - service specific string for url construction that targets the start date of data
                'start_date' (madatory with start_date_query) - String specifying the start date for data. (YYYY-MM-DD)
                'end_date_query' - service specific string for url construction that targets the end date of data
                'end_date' (madatory with end_date_query) - String specifying the end date for data. (YYYY-MM-DD)
                'site_status' - service specific string for url construction. Cannot be used with 'agency' key
                'agency' - service specific string for url construction. Cannot be used with 'site_status' key

    RETURNS:
        url - url to request for data 
"""


def url_construct(endpoint, params):
    # Construct request URL
    sites = ','.join(params['sites'])
    url = endpoint 
    if params.get('extra'):
        url += params['extra'] + params['format']
    else:
        url += params['format']
    if params.get('site_query'):
        url += params['site_query'] + sites
    if params.get('start_date_query'):
        url += params['start_date_query'] + params['start_date']
    if params.get('end_date_query'):
        url += params['end_date_query'] + params['end_date']
    # one or the other. Not both. 'site_status' and 'agency' keys should not be in the same params dict.
    if params.get('site_status'):
        url += params['site_status']
    elif params.get('agency'):
        url += params['agency']
    return url
