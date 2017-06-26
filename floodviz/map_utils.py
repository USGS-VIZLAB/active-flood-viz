import requests

def site_dict(site_list, url_prefix):
    """Puts site data into a dictionary

    Args:
        site_list: A list of site ids to be queried on NWIS
        url_prefix: The beginning of the NWIS url

    Returns:
        A dict containing various site information in a usable format.
    """

    # generate the string of site ids for the url
    id_input_string = ",".join(site_list)

    # create the url
    url = url_prefix + "/?format=rdb&sites=" + id_input_string + "&siteStatus=all"

    # get data from url
    req = requests.get(url)

    # put data into list
    data = req.text.splitlines()[29:]

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
           filename: the file to be written to
           data: the data to be written to the file
    """

    with open(filename, "w") as f:
        f.write("{ \"type\": \"FeatureCollection\", \"features\": [ \n")

        for i, datum in enumerate(data):
            f.write("{ \"type\": \"Feature\",\n \"geometry\": {\n \"type\": \"Point\",\n \"coordinates\" : "
                    "[" + datum.get('dec_long_va') + ", " + datum.get('dec_lat_va') + "]\n },\n")
            f.write(" \"properties\": {\n \"name\": \"" + datum.get('station_nm') + "\",\n \"id\": \""
                    + datum.get('site_no') + "\",\n \"huc\": \"" +
                    datum['huc_cd'] + "\" \n } \n }")
            # add a comma unless at end of list
            if data[i] != data[len(data) - 1]:
                f.write(",")
            f.write("\n")
        f.write(" ] }")