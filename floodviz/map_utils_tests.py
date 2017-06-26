from floodviz.map_utils import site_dict, write_geojson

import unittest

import requests
import requests_mock

sites = ['05463500', '05471050', '05420680', '05479000', '05484000', '05481000', '05486000', '05421000', '05485500',
            '05455100', '05470500', '05451500', '05458000', '05471000', '05462000', '05457700', '05458500', '05470000',
            '05484500', '05481300', '05464220', '05458900', '05485605', '05463000', '05471200', '05476750', '05411850',
            '05454220', '05481950', '05416900', '05464500', '05487470']

prefix = 'https://waterservices.usgs.gov/nwis/site'

url = "https://waterservices.usgs.gov/nwis/site/?format=rdb&sites=05463500,05471050,05420680,05479000,05484000," \
      "05481000,05486000,05421000,05485500,05455100,05470500,05451500,05458000,05471000,05462000,05457700,05458500," \
      "05470000,05484500,05481300,05464220,05458900,05485605,05463000,05471200,05476750,05411850,05454220,05481950," \
      "05416900,05464500,05487470&siteStatus=all"

mock_data = [{'agency_cd': 'USGS', 'site_no': '05411850', 'station_nm': 'Turkey River near Eldorado, IA',
              'site_tp_cd': 'ST', 'dec_lat_va': '43.0541879', 'dec_long_va': '-91.8090983', 'coord_acy_cd': '1',
              'dec_coord_datum_cd': 'NAD83', 'alt_va': ' 890.00', 'alt_acy_va': '.01', 'alt_datum_cd': 'NGVD29',
              'huc_cd': '07060004'}]


class TestSiteDict(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(site_dict([], prefix), None)

    def test_empty_url(self):
        self.assertEqual(site_dict(sites, ""), None)

    def test_bad_list(self):
        self.assertEqual(site_dict(['x'], prefix), None)

    def test_bad_list2(self):
        self.assertEqual(site_dict(['1234'], prefix), None)

    def test_bad_url(self):
        self.assertEqual(site_dict(sites, "x"), None)

    def test_bad_request_data(self):
        with requests_mock.Mocker() as m:
            m.get(url, text='resp')
            self.assertEqual(site_dict(sites, prefix), None)

    def test_bad_request_data2(self):
        with requests_mock.Mocker() as m:
            m.get(url, text='#')
            self.assertEqual(site_dict(sites, prefix), None)


class TestWriteGeojson(unittest.TestCase):

    def test_filename_is_string(self):
        self.assertEqual(write_geojson(1, mock_data), None)

    def test_data_is_none(self):
        self.assertEqual(write_geojson("out.json", None), None)

    def test_empty_data(self):
        self.assertEqual(write_geojson("out.json", []), None)

    def test_bad_filename_suffix(self):
        self.assertEqual(write_geojson("out.x", mock_data), None)

    def test_data_not_list(self):
        self.assertEqual(write_geojson("out.json", "string"), None)


if __name__ == '__main__':
    unittest.main()

