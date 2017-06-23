import requests

# function to generate a dictionary of site data after querying NWIS

def site_dict(site_list, url_prefix):
    # generate the string of site ids for the url
    id_input_string = ",".join(site_list)

    # create the url
    url = url_prefix + "/?format=rdb&sites=" + id_input_string + "&siteStatus=all"

    # get data from url
    data = ""
    req = requests.get(url)
    for line in req.text.splitlines():
        if not line.startswith("#"):
            data += line + '\n'

    # create array by splitting lines
    data = data.split('\n')

    # make a list of dicts  from data
    fields = data[0].split('\t')
    dnice = []
    for line in data[2:]:
        line = line.split('\t')
        line_dict = dict(zip(fields, line))
        dnice.append(line_dict)

    # remove bad element from end of list
    dnice = dnice[:-1]
    return dnice


# function to write data from NWIS to a geojson file
def write_geojson(filename, data):
    with open(filename, "w") as f:
        f.write("{ \"type\": \"FeatureCollection\", \"features\": [ \n")

        count = -1
        for datum in data:
            count += 1
            f.write("{ \"type\": \"Feature\",\n \"geometry\": {\n \"type\": \"Point\",\n \"coordinates\" : "
                    "[" + datum.get('dec_long_va') + ", " + datum.get('dec_lat_va') + "]\n },\n")
            f.write(" \"properties\": {\n \"name\": \"" + datum.get('station_nm') + "\",\n \"id\": \""
                    + datum.get('site_no') + "\",\n \"huc\": \"" +
                    datum['huc_cd'] + "\" \n } \n }")
            # add a comma unless at end of list
            if data[count] != data[len(data) - 1]:
                f.write(",")
            f.write("\n")
        f.write(" ] }")
