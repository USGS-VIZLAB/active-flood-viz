import unittest
import requests_mock
from floodviz.utils import parse_rdb


class TestRdbParse(unittest.TestCase):

    def setUp(self):
        self.mock_url = 'http://example.com/?format=rdb&sites=05420680,05463500&siteStatus=all'
        self.sites = ['05420680', '05463500']
        # self.endpoint = 'https://waterservices.usgs.gov/nwis/site/'
        self.endpoint_mock = 'http://example.com/'

        self.test_dict = {
            'format': 'rdb',
            'sites': ','.join(self.sites),
            'siteStatus': 'all'
        }

        self.valid_data = [
            {'agency_cd': 'USGS', 'site_no': '05420680', 'station_nm': 'Wapsipinicon River near Tripoli, IA',
             'site_tp_cd': 'ST', 'dec_lat_va': '42.83609117', 'dec_long_va': '-92.2574003', 'coord_acy_cd': 'F',
             'dec_coord_datum_cd': 'NAD83', 'alt_va': '986.42', 'alt_acy_va': '.01', 'alt_datum_cd': 'NGVD29',
             'huc_cd': '07080205'},
            {'agency_cd': 'USGS', 'site_no': '05463500', 'station_nm': 'Black Hawk Creek at Hudson, IA',
             'site_tp_cd': 'ST', 'dec_lat_va': '42.4077639', 'dec_long_va': '-92.4632451', 'coord_acy_cd': 'F',
             'dec_coord_datum_cd': 'NAD83', 'alt_va': '865.03', 'alt_acy_va': '.01', 'alt_datum_cd': 'NGVD29',
             'huc_cd': '07080102'}]

        self.response = '# \n' \
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
                        'coord_acy_cd\tdec_coord_datum_cd\talt_va\talt_acy_va\talt_datum_cd\thuc_cd\n' \
                        '5s\t15s\t50s\t7s\t16s\t16s\t1s\t10s\t8s\t3s\t10s\t16s \n' \
                        'USGS\t05420680\tWapsipinicon River near Tripoli, IA\tST\t42.83609117\t-92.2574003\t' \
                        'F\tNAD83\t986.42\t.01\tNGVD29\t07080205\n' \
                        'USGS\t05463500\tBlack Hawk Creek at Hudson, IA\tST\t42.4077639\t-92.4632451\t' \
                        'F\tNAD83\t865.03\t.01\tNGVD29\t07080102\n'

        self.no_data_response = '# \n' \
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
                        'coord_acy_cd\tdec_coord_datum_cd\talt_va\talt_acy_va\talt_datum_cd\thuc_cd\n' \
                        '5s\t15s\t50s\t7s\t16s\t16s\t1s\t10s\t8s\t3s\t10s\t16s \n' \


    def test_bad_request(self):
        with requests_mock.Mocker() as m:
            m.get(self.mock_url, status_code=404)
            self.assertEqual(parse_rdb(self.endpoint_mock, self.test_dict), None)

    def test_valid_data(self):
        with requests_mock.Mocker() as m:
            m.get(self.mock_url, text=self.response)
            self.assertEqual(parse_rdb(self.endpoint_mock, self.test_dict), self.valid_data)

    def test_no_data(self):
        with requests_mock.Mocker() as m:
            m.get(self.mock_url, text=self.no_data_response)
            self.assertEqual(parse_rdb(self.endpoint_mock, self.test_dict), [])
