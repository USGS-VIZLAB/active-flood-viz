from flask import render_template
import json
from . import app
from . import maputils


@app.route('/home/')
def home():
    return render_template('index.html')


@app.route('/map/')
def sitemap():
    site_data = maputils.site_dict(app.config['SITE_IDS'], app.config['NWIS_SITE_SERVICE_ENDPOINT'])
    site_data = maputils.create_geojson(site_data)
    projection = maputils.projection_info(app.config['PROJECTION_EPSG_CODE'], app.config['SPATIAL_REFERENCE_ENDPOINT'])
    return render_template('sitemap.html', site_data=site_data, proj4string=projection)
