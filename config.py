
DEBUG = False

NWIS_SITE_SERVICE_ENDPOINT = 'https://waterservices.usgs.gov/nwis/'

# Site IDs available for charting. Expects a list of valid site IDs.
SITE_IDS = []

# Start and end of time series data #
START_DT = ''
END_DT = ''

# Max amout of series to show on hydrograph after series filtering
N_SERIES = 5

# This dict holds aspect ratio data for hydrograph rendered in static/js/hydrograph.js. Keys are 'height' and 'width'
HYDRO_META = {}

# Map configuration

SPATIAL_REFERENCE_ENDPOINT = 'http://spatialreference.org/ref/epsg/${epsg_code}/proj4/'
PROJECTION_EPSG_CODE = '4326'

# with positive latitudes D3 looks at the southern hemisphere, so I invert them when defining MAP_CONFIG
BOUNDING_BOX = [-94.294625, 41.015733, -91.424186, 43.102420]

BACKGROUND_FILE = 'floodviz/static/geojson/states.json'
REFERENCE_FILE = 'floodviz/static/geojson/reference.json'
# this contains data that needs no further transformation before being sent to the javascript
MAP_CONFIG = {
    'width': 1000,
    'height': 600,
    'scale': 1,
    'bounds': [
        [BOUNDING_BOX[0], -BOUNDING_BOX[1]],
        [BOUNDING_BOX[2], -BOUNDING_BOX[3]]
    ]

}
