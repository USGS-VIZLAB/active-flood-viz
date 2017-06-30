DEBUG = False

NWIS_SITE_SERVICE_ENDPOINT = 'https://waterservices.usgs.gov/nwis/'
NWIS_WATERPEAK_SITE_SERVICE_ENDPOINT = 'https://nwis.waterdata.usgs.gov/nwis/peak'

### Hydrograph Config Vars ###

# Site IDs available for charting. Expects a list of valid site IDs. 
SITE_IDS = []

# Start and end of time series data for event hydrograph
EVENT_START_DT = ''
EVENT_END_DT = ''


# This dict holds aspect ratio data for hydrograph rendered in static/js/hydrograph.js. Keys are 'height' and 'width'
HYDRO_META = {}






### Peak Flow Config Vars ###

# Site ID for peak flow bar chart
PEAK_SITE = '' # used arbitrary site for now
# start date for peak flow values
PEAK_START_DT = ''
# end date for peak flow values
PEAK_END_DT = ''
# This dict holds aspect ratio data for the peak flow chart rendered in static/js/peakflow.js
PEAK_META = {}