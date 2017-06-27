import requests

def site_dict(site_list, url_prefix):
    """Puts site data into a dictionary
    Args:
        site_list: A list of site ids to be queried on NWIS
        url_prefix: A string containing the beginning of the NWIS site url
    Returns:
        An array of dicts containing various site information in a usable format.
    """

    # if not site_list:
    #     print("Error: site_list is empty")
    #     return

    # if not url_prefix:
    #     print("Error: url_prefix is empty")
    #     return

    # for site in site_list:
    #     if not site.isdigit():
    #         print("Error: list contains a non-numeric element")
    #         return
    #     if len(site) != 8:
    #         print("Error: all site ids must be 8 digits")
    #         return

    # if not url_prefix == 'https://waterservices.usgs.gov/nwis/site':
    #     print("Error: incorrect url prefix provided")
    #     return

    # generate the string of site ids for the url
    id_input_string = ",".join(site_list)

    # create the url
    url = url_prefix + "/?format=rdb&sites=" + id_input_string + "&siteStatus=all"

    # get data from url
    req = requests.get(url)

    if not req.text.startswith('#'):
        print("Error: request returns invalid data")
        return

    # put data into list
    data = []
    for line in req.text.splitlines():
        if not line.startswith('#'):
            data.append(line)

    if not data:
        print("Error: webpage contains no usable data")
        return

    # make a list of dicts from data
    fields = data[0].split('\t')
    dnice = []
    for line in data[2:]:
        line = line.split('\t')
        line_dict = dict(zip(fields, line))
        dnice.append(line_dict)

    return dnice


def write_geojson(filename, data):
    """Writes site data to a .json file so it can be mapped
       Args:
           filename: A string naming the file to be written to
           data: A list of dicts with data to be written to the file
    """
    if not type(filename) == str:
        print("Error: filename must be string")
        return;

    if not filename.endswith(".json"):
        print("Error: outfile must be .json")
        return

    if not data:
        print("Error: data is empty list")
        return

    if data is None:
        print("Error: data is None")
        return

    if not isinstance(data, list):
        print("Error: data is not a list")
        return

    with open(filename, "w") as f:
        f.write("{ \"type\": \"FeatureCollection\", \"features\": [ \n")

        for i, datum in enumerate(data):
            f.write("{ \"type\": \"Feature\",\n \"geometry\": {\n \"type\": \"Point\",\n \"coordinates\" : "
                    "[" + datum.get('dec_long_va') + ", " + datum.get('dec_lat_va') + "]\n },\n")
            f.write(" \"properties\": {\n \"name\": \"" + datum.get('station_nm') + "\",\n \"id\": \""
                    + datum.get('site_no') + "\",\n \"huc\": \"" +
                    datum.get('huc_cd') + "\" \n } \n }")
            # add a comma unless at end of list
            if data[i] != data[len(data) - 1]:
                f.write(",")
            f.write("\n")
        f.write(" ] }")