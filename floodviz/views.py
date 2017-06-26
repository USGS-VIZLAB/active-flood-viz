from flask import request, render_template, abort

from . import app
from . import maputils

@app.route('/home/')
def home():
    return render_template('index.html')


maputils.site_dict(app.config['SITE_IDS'], app.config['NWIS_SITE_SERVICE_ENDPOINT'])