from datetime import date
from statistics import mean

from . import app
from . import map_utils


def assemble():
    ld = {
        "@context": "http://schema.org",
        "@type": "WebSite",
        "name": "Active flood visualization",
        "about": "Visualization of a flood event based on USGS streamgage readings",
        "datePublished": str(date.today),
        "publisher": {
            "@context": "http://schema.org",
            "@type": "Organization",
            "name": "U.S. Geological Survey",
            "alternateName": "USGS"
        },
    }


def fetch_gage_data():
    gage_data = map_utils.site_dict(app.config['SITE_IDS'], app.config['SPATIAL_REFERENCE_ENDPOINT'])
    return gage_data


def assemble_gages():
    gage_data = fetch_gage_data()
    ld = []
    for gage in gage_data:
        gage_ld = {
            "@context": "http://schema.org",

        }

def assemble_event():
    start = app.config['EVENT_START_DT']
    end = app.config['EVENT_END_DT']

    lon = mean([app.config['BOUNDING_BOX'][0], app.config['BOUNDING_BOX'][2]])
    lat = mean([app.config['BOUNDING_BOX'][1], app.config['BOUNDING_BOX'][3]])

