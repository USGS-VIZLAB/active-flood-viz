import argparse
from floodviz import app as application
from flask_frozen import Freezer

import json

freezer = Freezer(application)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-ht', type=str)
    parser.add_argument('--port', '-p', type=str)
    parser.add_argument('--freeze', '-f', action='store_true', default=False)
    parser.add_argument('--norun', '-n', action='store_true', default=False)
    args = parser.parse_args()
    host_val = args.host
    port_val = args.port
    do_freeze = args.freeze
    run = not args.norun

    with open('floodviz/static/reference/reference.json', 'r') as f:
        data = json.load(f)

        # print(data)
        epsg = data['target_epsg'][5:]
        site_ids = data['site_ids']
        display_sites = data['display_sites']
        bbox = data['bbox']
        start_date = data['startDate']
        end_date = data['endDate']
        peak_dv_date = data['endDate']
        peak_site = data['peak']['site']
        # peak_start_date = data['peak']['startDate']
        # peak_end_date = data['peak']['endDate']
        # print(data['reference']['features'][0])

    for i in range(0, len(data['reference']['features'])):
        if data['reference']['features'][i]['properties']['reftype'] == 'rivers':
            print('river')
        if data['reference']['features'][i]['properties']['reftype'] == 'city':
            print('city')
        if data['reference']['features'][i]['properties']['reftype'] == 'politicalBoundaries':
            print('border')

    if host_val is not None:
        host = host_val
    else:
        host = '127.0.0.1'

    if port_val is not None:
        port = port_val
    else:
        port = 5050

    if do_freeze:
        print("freezing")
        freezer.freeze()
        print("frozen")
        if run:
            freezer.serve(host=host, port=port, threaded=True)
    else:
        application.run(host=host, port=port, threaded=True)
    # run from the command line as follows
    # python run.py -ht <ip address of your choice>