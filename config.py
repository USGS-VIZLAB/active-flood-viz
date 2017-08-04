import os

DEBUG = False

NWIS_SITE_SERVICE_ENDPOINT = 'https://waterservices.usgs.gov/nwis/'
NWIS_PEAK_STREAMFLOW_SERVICE_ENDPOINT = 'https://nwis.waterdata.usgs.gov/nwis/peak'


### Hydrograph Event Config Vars ###

# Site IDs available for charting. Expects a list of valid site IDs.
SITE_IDS = []

# the subset of site_ids to be displayed in the hydrograph by default.
HYDRO_DISPLAY_IDS = []

# Start and end of time series data for Flood Event. Format for dates: YYYY-MM-DD #
EVENT_START_DT = ''
EVENT_END_DT = ''

# This dict holds aspect ratio data for hydrograph rendered in static/js/hydrograph.js. Keys are 'height' and 'width'
CHART_DIMENSIONS = {}



### Peak Flow Config Vars ###

# Site ID for peak flow bar chart
PEAK_SITE = '' # used arbitrary site for now
# start date for peak flow values
PEAK_START_DT = ''
# end date for peak flow values
PEAK_END_DT = ''
# This dict holds aspect ratio data for the peak flow chart rendered in static/js/peakflow.js
PEAK_META = {}

# Map configuration

SPATIAL_REFERENCE_ENDPOINT = 'http://spatialreference.org/ref/epsg/${epsg_code}/proj4/'
PROJECTION_EPSG_CODE = '4326'

# Should be 4 numbers: x1, y1, x2, y2
BOUNDING_BOX = []

# paths to geojson files for background and reference locations
BACKGROUND_FILE = ''
RIVERS_FILE = ''
REFERENCE_DATA = None

# this contains data that needs no further transformation before being sent to the javascript
MAP_CONFIG = {
    'width': None,
    'height': None,
    'scale': None,
}

# Google Analytics
GA_ID = ""

deployed_url_base = os.environ.get('DEPLOYED_BASE_URL')
if deployed_url_base:
    FREEZER_BASE_URL = deployed_url_base
    print(FREEZER_BASE_URL)

thumbnail = os.environ.get('THUMBNAIL')
if thumbnail == "true":
    THUMBNAIL = True
else:
    THUMBNAIL = False