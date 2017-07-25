DEBUG = False

TITLE = 'Lorem Ipsum'
SUBTITLE = 'Lorem ipsum dolor sit amet'
FOOTER = 'loremipsum.com'

# dimensions for the hydrograph
HYDROGRAPH_ASPECT_RATIO = {
    'height': 3.5,
    'width': 5.5
}

MAP_CONFIG = {
    'width': 1,
    'height': 1,
    'scale': 1
}

# Site IDs available for charting
SITE_IDS = ['05463500', '05471050', '05420680', '05479000',
            '05484000', '05481000', '05486000', '05421000',
            '05485500', '05455100', '05470500', '05451500',
            '05458000', '05471000', '05462000', '05457700',
            '05458500', '05470000', '05484500', '05481300',
            '05464220', '05458900', '05485605', '05463000',
            '05471200', '05476750', '05411850', '05454220',
            '05481950', '05416900', '05464500', '05487470']

# Sites to be displayed on the hydrograph by default.
HYDRO_DISPLAY_IDS = ['05471200', '05476750', '05411850', '05454220',
                     '05481950', '05416900', '05464500', '05487470']


# Start and end of time series data #
EVENT_START_DT = '2008-06-26'
EVENT_END_DT = '2008-07-05'



# MAP SETTINGS

PROJECTION_EPSG_CODE = '2794'

BOUNDING_BOX = [-94.294625, 41.015733, -91.424186, 43.102420]

BACKGROUND_FILE = 'floodviz/static/geojson/states.json'
RIVERS_FILE = 'floodviz/static/geojson/rivers.json'





REFERENCE_DATA = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-91.67, 41.97]
            },
            "properties": {
                "name": "Cedar Rapids IA",
                "country.etc": "IA",
                "pop": "123243",
                "capital": "0"
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-93.62, 41.58]
            },
            "properties": {
                "name": "Des Moines IA",
                "country.etc": "IA",
                "pop": "192050",
                "capital": "2"
            }
        }
    ]
}

### Peak Flow Config Vars ###

# Site ID for peak flow bar chart
PEAK_SITE = '05481950'  # used arbitrary site for now --- 05458900
# Daily Value date for lollipop construction
PEAK_DV_DT = '2008-07-05'
# This dict holds aspect ratio data for the peak flow chart rendered in static/js/peakflow.js
# NOTE: the height and width of the svg are modified beyond these values in peakflow.js
PEAK_META = {
    'height': '4',
    'width': '7.5'
}
