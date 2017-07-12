import requests

"""
takes a web service endpoint, a dictionary of key/value pairs for the query parameters
and returns an array of dictionaries representing the data returned in the rdb file. 

"""

def parse_rdb(endpoint, params):
    pass





def url_construct(endpoint, params):
    ret = None
    # Construct request URL
    sites = ','.join(params['sites'])
    url = endpoint + params['format']
    if params.get('site_query'):
        url += params['site_query'] + sites
    if params.get('start_date_query'):
        url += params['start_date_query'] + params['start_date']
    if params.get('end_date_query'):
        url += params['end_date_query'] + params['end_date']
    if params.get('site_status'):
        url += params['site_status']
    elif params.get('agency'):
        url += params['agency']

    return url
