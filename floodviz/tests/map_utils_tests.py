import unittest

import requests_mock
from nose.tools import raises

from floodviz.map_utils import site_dict, create_geojson, projection_info, filter_background


class TestSiteDict(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.sites = ['05420680', '05463500']
        self.prefix = 'https://waterservices.usgs.gov/nwis/'
        self.request_url = "https://waterservices.usgs.gov/nwis/site/?format=rdb&sites=05420680,05463500&siteStatus=all"
        self.correct_output = [
            {
                'site_no': '05463500',
                'station_nm': 'Black Hawk Creek at Hudson, IA',
                'dec_lat_va': '42.4077639',
                'dec_long_va': '-92.4632451',
                'huc_cd': '07080102'
            },
            {
                'site_no': '05420680',
                'station_nm': 'Wapsipinicon River near Tripoli, IA',
                'dec_lat_va': '42.83609117',
                'dec_long_va': '-92.2574003',
                'huc_cd': '07080205'
            }
        ]
        # these are explicitly separated with tabs because they might otherwise be converted to spaces.
        self.NWIS_response = '# \n' \
                             '# \n' \
                             '# US Geological Survey \n' \
                             '# retrieved: 2017-06-30 11:12:17 -04:00 (vaas01) \n' \
                             '# \n' \
                             '# The Site File stores location and general information about groundwater, \n' \
                             '# surface water, and meteorological sites \n' \
                             '# for sites in USA. \n' \
                             '# \n' \
                             '# Lots of comment lines ... \n' \
                             '# \n' \
                             'agency_cd\tsite_no\tstation_nm\tsite_tp_cd\tdec_lat_va\tdec_long_va\t' \
                             'coord_acy_cd\tdec_coord_datum_cd\talt_va\talt_acy_va\talt_datum_cd\thuc_cd \n' \
                             '5s\t15s\t50s\t7s\t16s\t16s\t1s\t10s\t8s\t3s\t10s\t16s \n' \
                             'USGS\t05420680\tWapsipinicon River near Tripoli, IA\tST\t42.83609117\t-92.2574003\t' \
                             'F\tNAD83\t986.42\t.01\tNGVD29\t07080205 \n' \
                             'USGS\t05463500\tBlack Hawk Creek at Hudson, IA\tST\t42.4077639\t-92.4632451\t' \
                             'F\tNAD83\t865.03\t.01\tNGVD29\t07080102 \n'

        # Second site missing site_no
        self.bad_NWIS_response = '# \n' \
                                 '# \n' \
                                 '# US Geological Survey \n' \
                                 '# retrieved: 2017-06-30 11:12:17 -04:00 (vaas01) \n' \
                                 '# \n' \
                                 '# The Site File stores location and general information about groundwater, \n' \
                                 '# surface water, and meteorological sites \n' \
                                 '# for sites in USA. \n' \
                                 '# \n' \
                                 '# Lots of comment lines ... \n' \
                                 '# \n' \
                                 'agency_cd\tsite_no\tstation_nm\tsite_tp_cd\tdec_lat_va\tdec_long_va\t' \
                                 'coord_acy_cd\tdec_coord_datum_cd\talt_va\talt_acy_va\talt_datum_cd\thuc_cd \n' \
                                 '5s\t15s\t50s\t7s\t16s\t16s\t1s\t10s\t8s\t3s\t10s\t16s \n' \
                                 'USGS\t05420680\tWapsipinicon River near Tripoli, IA\tST\t42.83609117\t-92.2574003\t' \
                                 'F\tNAD83\t986.42\t.01\tNGVD29\t07080205 \n' \
                                 'USGS\tBlack Hawk Creek at Hudson, IA\tST\t42.4077639\t-92.4632451\t' \
                                 'F\tNAD83\t865.03\t.01\tNGVD29\t 07080102\n'

    def test_empty_list(self):
        with requests_mock.Mocker() as m:
            m.get(self.request_url, text=self.NWIS_response)
        self.assertEqual(site_dict([], self.prefix), [])

    def test_bad_status_code(self):
        with requests_mock.Mocker() as m:
            m.get(self.request_url, status_code=404)
            self.assertEqual(site_dict(self.sites, self.prefix), None)

    def test_good_data(self):
        with requests_mock.Mocker() as m:
            m.get(self.request_url, text=self.NWIS_response)
            actual_output = site_dict(self.sites, self.prefix)
            for item in actual_output:
                self.assertIn(item, self.correct_output)

    @raises(KeyError)
    def test_missing_field(self):
        with requests_mock.Mocker() as m:
            m.get(self.request_url, text=self.bad_NWIS_response)
            site_dict(self.sites, self.prefix)
            self.assertRaises(KeyError)


class TestCreateGeojson(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.input = [
            {
                'site_no': '05463500',
                'station_nm': 'Black Hawk Creek at Hudson, IA',
                'dec_lat_va': '42.4077639',
                'dec_long_va': '-92.4632451',
                'huc_cd': '07080102'
            },
            {
                'site_no': '05420680',
                'station_nm': 'Wapsipinicon River near Tripoli, IA',
                'dec_lat_va': '42.83609117',
                'dec_long_va': '-92.2574003',
                'huc_cd': '07080205'
            }
        ]
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
                        'huc': '07080102'
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
                        'huc': '07080205'
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


class TestFilterBackground(unittest.TestCase):
    def setUp(self):
        self.state_one = {
            'type': 'Feature',
            'properties': {
                'name': 'one'
            },
            'geometry': {
                'type': 'MultiPolygon',
                'coordinates': [
                    [[
                        [0, 0],
                        [0, 10],
                        [5, 10],
                        [0, 0]
                    ]],
                    [[
                        [5, 10],
                        [4.5, 10.5],
                        [4.8, 10.5],
                        [5, 10]
                    ]]
                ]
            }
        }
        self.state_two = {
            'type': 'Feature',
            'properties': {
                'name': 'two'
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [
                    [
                        [0, 10],
                        [5, 10],
                        [4.5, 10.5],
                        [4.8, 10.5],
                        [5, 10],
                        [5, 13],
                        [0, 13],
                        [0, 10]
                    ]
                ]
            }
        }
        self.state_three = {
            'type': 'Feature',
            'properties': {
                'name': 'three'
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [
                    [
                        [0, 0],
                        [7, 0],
                        [10, 7],
                        [5, 13],
                        [5, 10],
                        [0, 0]
                    ]
                ]
            }
        }
        self.state_four = {
            'type': 'Feature',
            'properties': {
                'name': 'four'
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [
                    [
                        [0, 0],
                        [-3, 0],
                        [-5, 7],
                        [0, 9],
                        [0, 0]
                    ]
                ]
            }
        }
        self.state_five = {
            'type': 'Feature',
            'properties': {
                'name': 'five'
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [
                    [
                        [-5, 7],
                        [-3, 13],
                        [0, 13],
                        [0, 9],
                        [-5, 7]
                    ]
                ]
            }
        }

        # A collection of 4 polygons and 1 multipolygon in a geojson-like dict
        self.states = {
            'type': 'FeatureCollection',
            'features': [
                self.state_one,
                self.state_two,
                self.state_three,
                self.state_four,
                self.state_five
            ]
        }

        # Bounding Boxes to test with
        self.bboxA = [4, 11, 6, 10.3]
        self.bboxB = [-2.5, 7.5, -1.5, 6]
        self.bboxC = [2, 2, 3, 3]

        # Correct output for each bbox
        # bboxA should be found to contain boundaries of states one, two, and three
        self.outputA = {
            'type': 'FeatureCollection',
            'features': [
                self.state_one,
                self.state_two,
                self.state_three
            ]
        }
        # bboxB should be contained by only state four
        self.outputB = {
            'type': 'FeatureCollection',
            'features': [
                self.state_four
            ]
        }
        # bboxC should be contained by states one and three
        self.outputC = {
            'type': 'FeatureCollection',
            'features': [
                self.state_one,
                self.state_three
            ]
        }

    def test_bboxA(self):
        actual = filter_background(self.bboxA, self.states)
        self.assertEqual(actual, self.outputA)

    def test_bboxB(self):
        actual = filter_background(self.bboxB, self.states)
        self.assertEqual(actual, self.outputB)

    def test_bboxC(self):
        actual = filter_background(self.bboxC, self.states)
        self.assertEqual(actual, self.outputC)
