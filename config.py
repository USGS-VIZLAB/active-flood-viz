
DEBUG = True

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

