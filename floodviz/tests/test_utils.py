import unittest
import requests_mock
from floodviz.utils import parse_rdb


class TestRdbParsePeak(unittest.TestCase):
    def setUp(self):
        self.peak_site = '05481950'
        self.peak_dv_date = '2008-07-05'
        self.peak_start_date = '2008-05-20'
        self.peak_end_date = '2008-07-05'
        self.endpoint_mock = 'http://somethingfake.notadomain/noob/'
        self.mock_url_peak = 'http://somethingfake.notadomain/noob/?format=rdb&site_no=05481950&start_date=' \
                             '2008-05-20&end_date=2008-07-05&agency_cd=USGS'
        self.mock_url_dv = 'http://somethingfake.notadomain/noob/?format=rdb&sites=05481950&startDT=' \
                           '2008-07-05&endDT=2008-07-05&siteStatus=all'
        self.test_dict_peak = {
            'format': 'rdb',
            'site_no': self.peak_site,
            'start_date': self.peak_start_date,
            'end_date': self.peak_end_date,
            'agency_cd': 'USGS'
        }
        self.test_dict_dv = {
            'format': 'rdb',
            'sites': self.peak_site,
            'startDT': self.peak_dv_date,
            'endDT': self.peak_dv_date,
            'siteStatus': 'all',
        }
        self.valid_return_peak = [
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1960-05-26', 'peak_tm': '', 'peak_va': '5480',
             'peak_cd': '', 'gage_ht': '14.05', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1961-06-08', 'peak_tm': '', 'peak_va': '1870',
             'peak_cd': '', 'gage_ht': '11.05', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1962-05-30', 'peak_tm': '', 'peak_va': '3780',
             'peak_cd': '', 'gage_ht': '12.90', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1963-08-07', 'peak_tm': '', 'peak_va': '2540',
             'peak_cd': '', 'gage_ht': '11.80', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1964-05-10', 'peak_tm': '', 'peak_va': '2010',
             'peak_cd': '', 'gage_ht': '11.25', 'gage_ht_cd': '2', 'year_last_pk': '', 'ag_dt': '1964-06-23',
             'ag_tm': '', 'ag_gage_ht': '11.70', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1965-04-02', 'peak_tm': '', 'peak_va': '4230',
             'peak_cd': '', 'gage_ht': '13.25', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1966-06-13', 'peak_tm': '', 'peak_va': '5470',
             'peak_cd': '', 'gage_ht': '14.04', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1967-06-10', 'peak_tm': '', 'peak_va': '4000',
             'peak_cd': '', 'gage_ht': '13.11', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1968-06-28', 'peak_tm': '', 'peak_va': '2000',
             'peak_cd': '', 'gage_ht': '11.24', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1969-03-19', 'peak_tm': '', 'peak_va': '4050',
             'peak_cd': '', 'gage_ht': '13.04', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1970-05-15', 'peak_tm': '', 'peak_va': '3810',
             'peak_cd': '', 'gage_ht': '12.97', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1971-02-20', 'peak_tm': '', 'peak_va': '1900',
             'peak_cd': '2', 'gage_ht': '13.35', 'gage_ht_cd': '1', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1972-08-04', 'peak_tm': '', 'peak_va': '1080',
             'peak_cd': '', 'gage_ht': '8.70', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1973-04-17', 'peak_tm': '', 'peak_va': '4130',
             'peak_cd': '', 'gage_ht': '12.94', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1974-05-19', 'peak_tm': '', 'peak_va': '7340',
             'peak_cd': '', 'gage_ht': '14.69', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1975-03-18', 'peak_tm': '', 'peak_va': '2500',
             'peak_cd': '2', 'gage_ht': '11.61', 'gage_ht_cd': '1', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1976-04-18', 'peak_tm': '', 'peak_va': '1960',
             'peak_cd': '', 'gage_ht': '9.62', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1977-08-28', 'peak_tm': '', 'peak_va': '852',
             'peak_cd': '', 'gage_ht': '7.81', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''}]
        self.valid_return_dv = [{'agency_cd': 'USGS', 'site_no': '05481950', 'datetime': '2008-07-05',
                                 '43051_00060_00003': '430', '43051_00060_00003_cd': 'A'}]
        self.response_peak = '#\n' \
                             '# U.S. Geological Survey\n' \
                             '# National Water Information System\n' \
                             '# Retrieved: 2017-07-17 14:51:53 EDT\n' \
                             '#\n' \
                             '# ---------------------------------- WARNING ----------------------------------------\n' \
                             '#\n' \
                             'agency_cd	site_no	peak_dt	peak_tm	peak_va	peak_cd	gage_ht	gage_ht_cd	year_last_pk	ag_dt	ag_tm	ag_gage_ht	ag_gage_ht_cd\n' \
                             '5s	15s	10d	6s	8s	27s	8s	13s	4s	10d	6s	8s	11s\n' \
                             'USGS	05481950	1960-05-26		5480		14.05						\n' \
                             'USGS	05481950	1961-06-08		1870		11.05						\n' \
                             'USGS	05481950	1962-05-30		3780		12.90						\n' \
                             'USGS	05481950	1963-08-07		2540		11.80						\n' \
                             'USGS	05481950	1964-05-10		2010		11.25	2		1964-06-23		11.70	\n' \
                             'USGS	05481950	1965-04-02		4230		13.25						\n' \
                             'USGS	05481950	1966-06-13		5470		14.04						\n' \
                             'USGS	05481950	1967-06-10		4000		13.11						\n' \
                             'USGS	05481950	1968-06-28		2000		11.24						\n' \
                             'USGS	05481950	1969-03-19		4050		13.04						\n' \
                             'USGS	05481950	1970-05-15		3810		12.97						\n' \
                             'USGS	05481950	1971-02-20		1900	2	13.35	1					\n' \
                             'USGS	05481950	1972-08-04		1080		8.70						\n' \
                             'USGS	05481950	1973-04-17		4130		12.94						\n' \
                             'USGS	05481950	1974-05-19		7340		14.69						\n' \
                             'USGS	05481950	1975-03-18		2500	2	11.61	1					\n' \
                             'USGS	05481950	1976-04-18		1960		9.62						\n' \
                             'USGS	05481950	1977-08-28		852		7.81						\n'
        self.response_dv = '# ---------------------------------- WARNING ----------------------------------------\n' \
                           '# Provisional data are subject to revision. Go to\n' \
                           '# http://help.waterdata.usgs.gov/policies/provisional-data-statement for more information.\n' \
                           '#\n' \
                           '# File-format description:  http://help.waterdata.usgs.gov/faq/about-tab-delimited-output\n' \
                           '# Automated-retrieval info: http://help.waterdata.usgs.gov/faq/automated-retrievals\n' \
                           '#' \
                           '# Contact:   gs-w_support_nwisweb@usgs.gov\n' \
                           '# retrieved: 2017-07-03 14:46:35 -04:00 (natwebvaas01)\n' \
                           '#\n' \
                           '# Data for the following 1 site(s) are contained in this file\n' \
                           '#    USGS 05481950 Beaver Creek near Grimes, IA\n' \
                           '# -----------------------------------------------------------------------------------\n' \
                           '#\n' \
                           '# TS_ID - An internal number representing a time series.\n' \
                           '# IV_TS_ID - An internal number representing the Instantaneous Value time series from which the daily' \
                           'statistic is calculated.\n' \
                           '#\n' \
                           '# Data provided for site 05481950\n' \
                           '#    TS_ID       Parameter    Statistic  IV_TS_ID       Description\n' \
                           '#    43051       00060        00003      44227          Discharge, cubic feet per second (Mean)\n' \
                           '#\n' \
                           '# Data-value qualification codes included in this output:\n' \
                           '#     A  Approved for publication -- Processing and review completed.\n' \
                           '#\n' \
                           'agency_cd\tsite_no\tdatetime\t43051_00060_00003\t43051_00060_00003_cd\n' \
                           '5s      15s     20d     14n     10s\n' \
                           'USGS\t05481950\t2008-07-05\t430\tA'

    def test_bad_request(self):
        with requests_mock.Mocker() as m:
            m.get(self.mock_url_peak, status_code=404)
            self.assertEqual(parse_rdb(self.endpoint_mock, self.test_dict_peak), None)

    def test_valid_data_peak(self):
        with requests_mock.Mocker() as m:
            m.get(self.mock_url_peak, text=self.response_peak)
            self.assertEqual(parse_rdb(self.endpoint_mock, self.test_dict_peak), self.valid_return_peak)

    def test_valid_data_dv(self):
        with requests_mock.Mocker() as m:
            m.get(self.mock_url_dv, text=self.response_dv)
            self.assertEqual(parse_rdb(self.endpoint_mock, self.test_dict_dv), self.valid_return_dv)


class TestRdbParseMap(unittest.TestCase):
    def setUp(self):
        self.mock_url = 'http://somethingfake.notadomain/noob/?format=rdb&sites=05420680,05463500&siteStatus=all'
        self.sites = ['05420680', '05463500']
        self.endpoint = 'https://waterservices.usgs.gov/nwis/site/'
        self.endpoint_mock = 'http://somethingfake.notadomain/noob/'
        self.header_values = {'site_no': 0,
                              'station_nm': 0,
                              'dec_long_va': 0,
                              'dec_lat_va': 0,
                              'huc_cd': 0
                              }
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

    def test_bad_request(self):
        with requests_mock.Mocker() as m:
            m.get(self.mock_url, status_code=404)
            self.assertEqual(parse_rdb(self.endpoint_mock, self.test_dict), None)

    def test_valid_data(self):
        with requests_mock.Mocker() as m:
            m.get(self.mock_url, text=self.response)
            self.assertEqual(parse_rdb(self.endpoint_mock, self.test_dict), self.valid_data)
