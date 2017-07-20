import requests


def parse_rdb(endpoint, params):
    """
        Takes a web service endpoint, a dictionary of key/value pairs for the query parameters
        and returns all parsed data from the webservice.

        ARGS:
            endpoint - String specifying the web service url
            params - dictionary holding url parameters
                * keys for params should be the value you variable name for the query parameter
                  you want to specify. Values for these keys should be the query parameter value
                  you wish to use.

                  i.e {'site_no' : '056777781'} -> '&site_no=056777781'

        RETURNS:
            url - url to request for data
    """
    all_data = []
    try:
        r = requests.get(endpoint, params)
    except requests.exceptions.RequestException as e:
        print(e)
        print('- bad webservice url -')
    else:
        if r.status_code is 200:
            content = iter(r.text.splitlines())
            headers = None
            for line in content:
                # Skip commented lines
                if line.startswith('#'):
                    continue
                if headers is None:
                    # header procedure
                    line = line.split('\t')
                    headers = line
                    # Skip weird '5s      15s     20d     14n     10s\n'\' which appears on next line after headers
                    next(content)
                else:
                    # extraction procedure
                    line = line.split('\t')
                    data_point = {}
                    # sanity check that headers has been filled
                    if headers is not None:
                        for idx, data in enumerate(line):
                            data_point[headers[idx]] = data
                        all_data.append(data_point)
        else:
            all_data = None

    return all_data

