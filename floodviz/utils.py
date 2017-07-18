import requests


def parse_rdb(endpoint, params):
    """
        Takes a web service endpoint, a dictionary of key/value pairs for the query parameters
        and returns all parsed data from the webservice.

        ARGS:
            endpoint - String specifiying the web service url
            params - dictionary holding url parameters

                possible keys:
                    'sites' (mandatory) - List of string site_ids
                    'site_query' (mandatory) - service specific string for url construction that targets the sites.
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
    all_data = []
    sites = None
    url = endpoint
    data_format = '?format=rdb'
    if params.get('sites') is not None:
        sites = ','.join(params['sites'])
        if params.get('extra'):
            url += params['extra'] + data_format
        else:
            url += data_format
    # Needed
    if params.get('site_query'):
        url += params['site_query'] + sites
    # Can have one or the other or both for a valid url
    if params.get('start_date_query'):
        url += params['start_date_query'] + params['start_date']
    if params.get('end_date_query'):
        url += params['end_date_query'] + params['end_date']
    # One or the other here. Not both. 'site_status' and 'agency' keys should not be in the same params dict.
    if params.get('site_status'):
        url += params['site_status']
    elif params.get('agency'):
        url += params['agency']
    # request url
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        print('- bad webservice url -')
    else:
        if r.status_code is 200:
            content = r.text.splitlines()
            headers = None
            for line in content:
                # Skip commented lines
                if line.startswith('#'):
                    continue
                if line.startswith('USGS'):
                    # extraction procedure
                    line = line.split('\t')
                    data_point = {}
                    # sanity check that headers has been filled
                    if headers is not None:
                        for idx, data in enumerate(line):
                            data_point[headers[idx]] = data
                        all_data.append(data_point)
                # Should run before above if block
                elif headers is None:
                    # header procedure
                    line = line.split('\t')
                    headers = line
        else:
            all_data = None

    return all_data

