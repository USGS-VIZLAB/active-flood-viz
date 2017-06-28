from floodviz.map_utils import site_dict, write_geojson

import unittest

import requests_mock

# url = "https://waterservices.usgs.gov/nwis/site/?format=rdb&sites=05463500,05471050,05420680,05479000&siteStatus=all"
#
# mock_data = [{'agency_cd': 'USGS', 'site_no': '05411850', 'station_nm': 'Turkey River near Eldorado, IA',
#               'site_tp_cd': 'ST', 'dec_lat_va': '43.0541879', 'dec_long_va': '-91.8090983', 'coord_acy_cd': '1',
#               'dec_coord_datum_cd': 'NAD83', 'alt_va': ' 890.00', 'alt_acy_va': '.01', 'alt_datum_cd': 'NGVD29',
#               'huc_cd': '07060004'}]


class TestSiteDict(unittest.TestCase):

    def setUp(self):
        self.sites = ['05420680', '05463500']
        self.prefix = 'https://waterservices.usgs.gov/nwis/'
        self.good_return = [{'agency_cd': 'USGS', 'site_no': '05420680',
                             'station_nm': 'Wapsipinicon River near Tripoli, IA', 'site_tp_cd': 'ST',
                             'dec_lat_va': '42.83609117', 'dec_long_va': '-92.2574003', 'coord_acy_cd': 'F',
                             'dec_coord_datum_cd': 'NAD83', 'alt_va': ' 986.42', 'alt_acy_va': '.01',
                             'alt_datum_cd': 'NGVD29', 'huc_cd': '07080102'},
                            {'agency_cd': 'USGS', 'site_no': '05463500', 'station_nm': 'Black Hawk Creek at Hudson, IA',
                             'site_tp_cd': 'ST', 'dec_lat_va': '42.4077639', 'dec_long_va': '-92.4632451',
                             'coord_acy_cd': 'F', 'dec_coord_datum_cd': 'NAD83', 'alt_va': ' 865.03',
                             'alt_acy_va': '.01', 'alt_datum_cd': 'NGVD29', 'huc_cd': '07080205'}]

    def test_empty_list(self):
        self.assertEqual(site_dict([], self.prefix), [])

    def test_good_data(self):
        self.assertEqual(site_dict(self.sites, self.prefix), self.good_return)

    # def test_missing_fields(self):


# class TestWriteGeojson(unittest.TestCase):

if __name__ == '__main__':
    unittest.main()

