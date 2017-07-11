import requests

"""
takes a web service endpoint, a dictionary of key/value pairs for the query parameters
and returns an array of dictionaries representing the data returned in the rdb file. 

"""

def parse_rdb(endpoint, params):

    ret = None
    # Construct request URL
    sites = ','.join(params['sites'])
    url = endpoint + params['format'] + params['site_query'] + sites + params['end_date_query'] + params['end_date'] + params['agency']
    print(url)


    