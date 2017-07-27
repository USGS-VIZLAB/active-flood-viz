from flask import Flask

from . import reference_parser as ref

app = Flask(__name__.split()[0], instance_relative_config=True)

# Loads configuration information from config.py and instance/config.py
app.config.from_object('config')
app.config.from_pyfile('config.py')

REFERENCE_DATA = ref.parse_reference_data('examples/reference.json')

import floodviz.views

