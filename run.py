import argparse
from floodviz import app as application
from flask_frozen import Freezer

freezer = Freezer(application)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-ht', type=str)
    parser.add_argument('--port', '-p', type=str)
    parser.add_argument('--freeze', '-f', action='store_true', default=False)
    args = parser.parse_args()
    host_val = args.host
    port_val = args.port
    do_freeze = args.freeze

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
        freezer.serve(host=host, port=port, threaded=True)
    else:
        application.run(host=host, port=port, threaded=True)
    # run from the command line as follows
    # python run.py -ht <ip address of your choice>