import requests



def parse_rdb(endpoint, params):
    pass



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
