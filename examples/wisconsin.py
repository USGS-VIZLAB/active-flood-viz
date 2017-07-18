DEBUG = False

# Site IDs available for charting
SITE_IDS = ['05543830', '04087088', '04087233', '04087240',
            '04087204', '04087257', '04087220', '05544348',
            '05544475', '05544385', '04087120']

# Sites to be displayed on the hydrograph by default.
HYDRO_DISPLAY_IDS = SITE_IDS

# Start and end of time series data #
EVENT_START_DT = '2017-07-01'
EVENT_END_DT = '2017-07-17'

# dimensions for the hydrograph
CHART_DIMENSIONS = {
    'height': 400,
    'width': 800
}

# MAP SETTINGS

PROJECTION_EPSG_CODE = '2289'

BOUNDING_BOX = [-88.45, 43.1, -87.64, 42.55]

BACKGROUND_FILE = 'floodviz/static/geojson/states.json'
RIVERS_FILE = 'floodviz/static/geojson/rivers_SE_WI_2.json'

MAP_CONFIG = {
    'width': 750,
    'height': 450,
    'scale': 1,
    'debug': DEBUG,
}

REFERENCE_DATA = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-88.3072412, 42.67262837]
            },
            "properties": {
                "name": "Burlington WI"
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-88.2743512, 43.0052861]
            },
            "properties": {
                "name": "Waukesha WI"
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-87.8580761, 42.729738]
            },
            "properties": {
                "name": "Racine WI"
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-88.1075113, 43.057806]
            },
            "properties": {
                "name": "Milwaukee WI"
            }
        }
    ]
}

### Peak Flow Config Vars ###

# Site ID for peak flow bar chart
PEAK_SITE = '05543830'  # used arbitrary site for now --- 05458900
# Daily Value date for lollipop construction
PEAK_DV_DT = '2017-07-12'
# This dict holds aspect ratio data for the peak flow chart rendered in static/js/peakflow.js
# NOTE: the height and width of the svg are modified beyond these values in peakflow.js
PEAK_META = {
    'height': '300',
    'width': '900'
}