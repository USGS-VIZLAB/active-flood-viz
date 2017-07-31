import requests


def parse_rdb(endpoint, params):
    """
        Takes a web service endpoint, a dictionary of key/value pairs for the query parameters
        and returns all parsed data from the webservice.

        ARGS:
            endpoint - String specifying the web service url
            params - dictionary holding query parameters
                * keys for params should be the value you variable name for the query parameter
                  you want to specify. Values for these keys should be the query parameter value
                  you wish to use.

                  i.e {'site_no' : '056777781'} -> '&site_no=056777781'

        RETURNS:
            With success this function returns a list of data point dicts extracted from webservice.
            On a request failure, this function returns None.
    """
    all_data = []
    try:
        r = requests.get(endpoint, params)
    except requests.exceptions.RequestException as e:
        print(e)
        print('- bad webservice url -')
        all_data = None
    else:
        if r.status_code is 200:
            content = iter(r.text.splitlines())
            headers = None
            for line in content:
                # Skip commented lines
                if line.startswith('#') and headers is None:
                    continue
                if headers is None:
                    # header procedure
                    line = line.split('\t')
                    headers = [l.strip() for l in line]
                    next(content)
                else:
                    # extraction procedure
                    line = line.split('\t')
                    line = [l.strip() for l in line]
                    # sanity check that headers has been filled
                    if headers is not None:
                        data_point = zip(headers, line)
                        all_data.append(dict(data_point))
        else:
            all_data = None

    return all_data

