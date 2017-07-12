import unittest
import requests_mock
from floodviz.utils import parse_rdb, url_construct

class TestPeakUtilsRDBparse(unittest.TestCase):
    
    def setUp(self):
        self.peak_site = '05481950'
        self.peak_dv_date = '2008-07-05'
        self.peak_start_date = '2008-05-20'
        self.peak_end_date = '2008-07-05'
        self.endpoint = 'https://nwis.waterdata.usgs.gov/nwis/peak'
        self.test_dict = {
                 'sites': [self.peak_site],
                 'site_query': '&site_no=',
                 'start_date': self.peak_start_date,
                 'start_date_query': '&start_date=',
                 'end_date': self.peak_end_date,
                 'peak_dv_date': self.peak_dv_date,
                 'end_date_query': '&end_date=',
                 'format': '?format=rdb',
                 'agency': '&agency_cd=USGS'
                }
    def test_bad_request(self):
        pass
        # with requests_mock.Mocker() as m:
        #     m.get(self.mock_url, status_code=404)
        #     self.assertEqual(req_peak_data(self.site, self.P_START_DT, self.P_END_DT, self.prefix), None)

class TestPeakUtilsURLconstruct(unittest.TestCase):
    
    def setUp(self):
        self.peak_site = '05481950'
        self.peak_dv_date = '2008-07-05'
        self.peak_start_date = '2008-05-20'
        self.peak_end_date = '2008-07-05'
        self.endpoint_peak = 'https://nwis.waterdata.usgs.gov/nwis/peak'
        self.endpoint_dv = 'https://waterservices.usgs.gov/nwis/'
        self.url_valid_peak = self.endpoint_peak + '?format=rdb' + '&site_no=' + self.peak_site + \
        '&start_date=' + self.peak_start_date + '&end_date=' + self.peak_end_date +'&agency_cd=USGS'
        self.url_valid_dv = self.endpoint_dv + 'dv?format=rdb' + '&sites=' + self.peak_site + \
        '&startDT=' + self.peak_dv_date + '&endDT=' + self.peak_dv_date + '&siteStatus=all'
        self.test_dict_peak = {
                 'sites': [self.peak_site],
                 'site_query': '&site_no=',
                 'start_date': self.peak_start_date,
                 'start_date_query': '&start_date=',
                 'end_date': self.peak_end_date,
                 'end_date_query': '&end_date=',
                 'format': '?format=rdb',
                 'agency': '&agency_cd=USGS'
                }
        self.test_dict_dv = {
                 'sites': [self.peak_site],
                 'site_query': '&sites=',
                 'start_date': self.peak_dv_date,
                 'start_date_query': '&startDT=',
                 'end_date': self.peak_dv_date,
                 'end_date_query': '&endDT=',
                 'format': '?format=rdb',
                 'site_status': '&siteStatus=all',
                 'extra' : 'dv'
                }
    
    def test_valid_url_peak(self):
        url = url_construct(self.endpoint_peak, self.test_dict_peak)
        self.assertEqual(url, self.url_valid_peak)

    def test_valid_url_dv(self):
        url = url_construct(self.endpoint_dv, self.test_dict_dv)
        self.assertEqual(url, self.url_valid_dv)



    

class TestMapUtilsRDBparse(unittest.TestCase):
    
    def setUp(self):
        self.sites = ['05420680', '05463500']
        self.endpoint = 'https://waterservices.usgs.gov/nwis/'
        self.test_dict = {
                 'sites': self.sites,
                 'site_query': '&sites=',
                 'site_status': '&siteStatus=all',
                 'format': '?format=rdb',
                 'extra' : 'site/'
                }



class TestMapUtilsURLconstruct(unittest.TestCase):
    
    def setUp(self):
        self.sites = ['05420680', '05463500']
        self.endpoint = 'https://waterservices.usgs.gov/nwis/'
        self.url_valid = 'https://waterservices.usgs.gov/nwis/site/?format=rdb&sites=05420680,05463500&siteStatus=all'
        self.test_dict = {
                 'sites': self.sites,
                 'site_query': '&sites=',
                 'site_status': '&siteStatus=all',
                 'format': '?format=rdb',
                 'extra' : 'site/'
                }
    
    def test_valid_url(self):
        url = url_construct(self.endpoint, self.test_dict)
        self.assertEqual(url, self.url_valid)
        
