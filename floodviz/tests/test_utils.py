import unittest
import requests_mock
from floodviz.utils import parse_rdb

class TestPeakUtilsRDB(unittest.TestCase):
    
    def setUp(self):
        self.test_dict = {
                 'sites': [peak_site],
                 'site_query': '&site_no=',
                 'start_date': peak_start_date,
                 'start_date_query': '&start_date=',
                 'end_date': peak_end_date,
                 'peak_dv_date': peak_dv_date,
                 'end_date_query': '&end_date=',
                 'format': '?format=rdb',
                 'agency': '&agency_cd=USGS'
                }
        self.peak_site = '05481950'
        self.peak_dv_date = '2008-07-05'
        self.peak_start_date = '2008-05-20'
        self.peak_end_date = '2008-07-05'
        self.endpoint = 'https://nwis.waterdata.usgs.gov/nwis/peak'

class TestMapUtilsRDB(unittest.TestCase):
    
    def setUp():
        self.test_dict = {
                 'sites': [peak_site],
                 'site_query': '&site_no=',
                 'start_date': peak_start_date,
                 'start_date_query': '&start_date=',
                 'end_date': peak_end_date,
                 'peak_dv_date': peak_dv_date,
                 'end_date_query': '&end_date=',
                 'format': '?format=rdb',
                 'agency': '&agency_cd=USGS'
                }
        self.sites = ['05420680', '05463500']
        self.endpoint = 'https://waterservices.usgs.gov/nwis/'