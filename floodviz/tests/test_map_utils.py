from floodviz.map_utils import alt_site_dict, create_geojson, projection_info

import unittest

import requests_mock

LIST_OF_SITE_DICTS = [
    {
        'site_no': '05463500',
        'station_nm': 'Black Hawk Creek at Hudson, IA',
        'dec_lat_va': '42.4077639',
        'dec_long_va': '-92.4632451',
        'huc_cd': None
    },
    {
        'site_no': '05420680',
        'station_nm': 'Wapsipinicon River near Tripoli, IA',
        'dec_lat_va': '42.83609117',
        'dec_long_va': '-92.2574003',
        'huc_cd': None
    }
]


class TestSiteDict(unittest.TestCase):
    def setUp(self):
        self.sites = ['05420680', '05463500']
        self.prefix = 'https://waterservices.usgs.gov/nwis/'

        self.NWIS_url = 'https://waterservices.usgs.gov/nwis/site/?format=mapper&sites=05420680,05463500&siteStatus=all'

        self.NWIS_response = '<mapper>' \
                             '<sites>' \
                             '<site ' \
                             'sno="05463500" ' \
                             'sna="Black Hawk Creek at Hudson, IA" ' \
                             'cat="ST" ' \
                             'lat="42.4077639" ' \
                             'lng="-92.4632451" ' \
                             'agc="USGS"' \
                             '/>' \
                             '<site ' \
                             'sno="05420680" ' \
                             'sna="Wapsipinicon River near Tripoli, IA" ' \
                             'cat="ST" ' \
                             'lat="42.83609117" ' \
                             'lng="-92.2574003" ' \
                             'agc="USGS"' \
                             '/>' \
                             '</sites>' \
                             '</mapper>'
        self.correct_output = LIST_OF_SITE_DICTS

    def test_empty_list(self):
        self.assertEqual(alt_site_dict([], self.prefix), [])

    def test_bad_status_code(self):
        with requests_mock.Mocker() as m:
            m.get(self.NWIS_url, status_code=404)
            self.assertEqual(alt_site_dict(self.sites, self.prefix), [])

    def test_good_data(self):
        with requests_mock.Mocker() as m:
            m.get(self.NWIS_url, text=self.NWIS_response)
            self.assertEqual(alt_site_dict(self.sites, self.prefix), self.correct_output)


class TestCreateGeojson(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.input = LIST_OF_SITE_DICTS
        self.correct_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [
                            '-92.4632451',
                            '42.4077639'
                        ]
                    },
                    'properties': {
                        'name': 'Black Hawk Creek at Hudson, IA',
                        'id': '05463500',
                        'huc': None
                    }
                },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [
                            '-92.2574003',
                            '42.83609117'
                        ]
                    },
                    'properties': {
                        'name': 'Wapsipinicon River near Tripoli, IA',
                        'id': '05420680',
                        'huc': None
                    }
                },
            ]
        }
        self.empty_geojson = {
            "type": "FeatureCollection",
            "features": []
        }

    def test_normal_case(self):
        self.assertEqual(create_geojson(self.input), self.correct_geojson)

    def test_empty_input(self):
        self.assertEqual(create_geojson([]), self.empty_geojson)

class TestProjectionInfo(unittest.TestCase):

    def setUp(self):
        self.spacial_ref_url = 'http://spatialreference.org/ref/epsg/3582/proj4/'
        self.spacial_ref_response = '+proj=lcc ' \
                                    '+lat_1=39.45 +lat_2=38.3 ' \
                                    '+lat_0=37.66666666666666 +lon_0=-77 ' \
                                    '+x_0=399999.9998983998 +y_0=0 ' \
                                    '+ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +to_meter=0.3048006096012192 +no_defs'

        self.url_template = 'http://spatialreference.org/ref/epsg/${epsg_code}/proj4/'
        self.code = '3582'
        self.correct_output = self.spacial_ref_response

    def test_bad_response(self):
        with requests_mock.Mocker() as m:
            m.get(self.spacial_ref_url, status_code=404)
            self.assertIsNone(projection_info(self.code, self.url_template))

    def test_normal_case(self):
        with requests_mock.Mocker() as m:
            m.get(self.spacial_ref_url, text=self.spacial_ref_response)
            self.assertEqual(projection_info(self.code, self.url_template), self.correct_output)

