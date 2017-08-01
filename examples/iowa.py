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

# This dict holds aspect ratio data for the peak flow chart rendered in static/js/peakflow.js
# NOTE: the height and width of the svg are modified beyond these values in peakflow.js
PEAK_META = {
    'height': '4',
    'width': '7.5'
}

# Thumbnail Support
THUMBNAIL = False