import unittest
import requests_mock
from floodviz.utils import parse_rdb


class TestPeakUtilsRDBparse(unittest.TestCase):

    def setUp(self):
        self.peak_site = '05481950'
        self.peak_dv_date = '2008-07-05'
        self.peak_start_date = '2008-05-20'
        self.peak_end_date = '2008-07-05'
        self.endpoint_peak = 'https://nwis.waterdata.usgs.gov/nwis/peak'
        self.endpoint_dv = 'https://waterservices.usgs.gov/nwis/'
        self.endpoint_mock = 'http://somethingfake.notadomain/noob/'
        self.mock_url_peak = 'http://somethingfake.notadomain/noob/?format=rdb&site_no=05481950&start_date='\
            '2008-05-20&end_date=2008-07-05&agency_cd=USGS'
        self.mock_url_dv = 'http://somethingfake.notadomain/noob/dv?format=rdb&sites=05481950&startDT='\
            '2008-07-05&endDT=2008-07-05&siteStatus=all'
        self.header_values_peak = {'site_no': 0, 'peak_dt': 0, 'peak_va': 0}
        self.header_values_dv = {'site_no': 0, 'datetime': 0, '43051_00060_00003': 0}
        self.url_valid_peak = self.endpoint_peak + '?format=rdb' + '&site_no=' + self.peak_site + \
            '&start_date=' + self.peak_start_date + '&end_date=' + self.peak_end_date + '&agency_cd=USGS'
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
            'extra': 'dv'
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
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1978-03-21', 'peak_tm': '', 'peak_va': '2980',
             'peak_cd': '', 'gage_ht': '11.38', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1979-03-20', 'peak_tm': '', 'peak_va': '4700',
             'peak_cd': '', 'gage_ht': '13.88', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1980-06-04', 'peak_tm': '', 'peak_va': '1730',
             'peak_cd': '', 'gage_ht': '9.02', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1981-08-14', 'peak_tm': '', 'peak_va': '1140',
             'peak_cd': '', 'gage_ht': '7.71', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1982-05-28', 'peak_tm': '', 'peak_va': '2780',
             'peak_cd': '', 'gage_ht': '11.32', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1983-06-29', 'peak_tm': '', 'peak_va': '3130',
             'peak_cd': '', 'gage_ht': '12.41', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1984-05-02', 'peak_tm': '', 'peak_va': '3220',
             'peak_cd': '', 'gage_ht': '11.76', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1984-12-28', 'peak_tm': '', 'peak_va': '1120',
             'peak_cd': '', 'gage_ht': '7.66', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1986-06-30', 'peak_tm': '', 'peak_va': '7980',
             'peak_cd': '', 'gage_ht': '14.73', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1987-08-28', 'peak_tm': '', 'peak_va': '2610',
             'peak_cd': '', 'gage_ht': '11.50', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1987-11-30', 'peak_tm': '', 'peak_va': '544',
             'peak_cd': '', 'gage_ht': '6.34', 'gage_ht_cd': '2', 'year_last_pk': '', 'ag_dt': '1988-02-01',
             'ag_tm': '', 'ag_gage_ht': '6.91', 'ag_gage_ht_cd': '1'},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1989-02-01', 'peak_tm': '', 'peak_va': '1540',
             'peak_cd': '2', 'gage_ht': '11.35', 'gage_ht_cd': '1', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1990-06-19', 'peak_tm': '', 'peak_va': '5580',
             'peak_cd': '', 'gage_ht': '14.20', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1991-06-16', 'peak_tm': '', 'peak_va': '3340',
             'peak_cd': '', 'gage_ht': '11.96', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1992-04-23', 'peak_tm': '', 'peak_va': '1790',
             'peak_cd': '', 'gage_ht': '9.76', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1993-07-10', 'peak_tm': '', 'peak_va': '14300',
             'peak_cd': '', 'gage_ht': '16.58', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1994-03-06', 'peak_tm': '', 'peak_va': '1580',
             'peak_cd': '', 'gage_ht': '9.24', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1995-05-30', 'peak_tm': '', 'peak_va': '1960',
             'peak_cd': '', 'gage_ht': '10.12', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1996-05-10', 'peak_tm': '', 'peak_va': '1410',
             'peak_cd': '', 'gage_ht': '8.88', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1997-07-24', 'peak_tm': '', 'peak_va': '1920',
             'peak_cd': '', 'gage_ht': '9.97', 'gage_ht_cd': '2', 'year_last_pk': '', 'ag_dt': '1997-02-20',
             'ag_tm': '', 'ag_gage_ht': '10.50', 'ag_gage_ht_cd': '1'},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1998-06-17', 'peak_tm': '', 'peak_va': '4280',
             'peak_cd': '', 'gage_ht': '13.20', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '1999-06-12', 'peak_tm': '', 'peak_va': '3820',
             'peak_cd': '', 'gage_ht': '12.36', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '2000-07-05', 'peak_tm': '', 'peak_va': '533',
             'peak_cd': '', 'gage_ht': '6.36', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '2001-03-17', 'peak_tm': '', 'peak_va': '2350',
             'peak_cd': '', 'gage_ht': '10.90', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '2002-05-30', 'peak_tm': '', 'peak_va': '912',
             'peak_cd': '', 'gage_ht': '7.55', 'gage_ht_cd': '2', 'year_last_pk': '', 'ag_dt': '2002-05-13',
             'ag_tm': '', 'ag_gage_ht': '7.70', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '2003-05-06', 'peak_tm': '', 'peak_va': '3160',
             'peak_cd': '', 'gage_ht': '11.99', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '2004-05-24', 'peak_tm': '', 'peak_va': '7300',
             'peak_cd': '', 'gage_ht': '14.59', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '2005-05-14', 'peak_tm': '', 'peak_va': '2530',
             'peak_cd': '', 'gage_ht': '11.19', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '2006-09-14', 'peak_tm': '04:30', 'peak_va': '1740',
             'peak_cd': '', 'gage_ht': '9.47', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '2007-04-27', 'peak_tm': '', 'peak_va': '6850',
             'peak_cd': '', 'gage_ht': '13.86', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''},
            {'agency_cd': 'USGS', 'site_no': '05481950', 'peak_dt': '2008-06-01', 'peak_tm': '', 'peak_va': '7800',
             'peak_cd': '', 'gage_ht': '14.51', 'gage_ht_cd': '', 'year_last_pk': '', 'ag_dt': '', 'ag_tm': '',
             'ag_gage_ht': '', 'ag_gage_ht_cd': ''}]
        self.valid_return_dv = [{'agency_cd': 'USGS', 'site_no': '05481950', 'datetime': '2008-07-05',
                                 '43051_00060_00003': '430', '43051_00060_00003_cd': 'A'}]
        self.response_peak = '#\n'\
            '# U.S. Geological Survey\n'\
            '# National Water Information System\n'\
            '# Retrieved: 2017-07-17 14:51:53 EDT\n'\
            '#\n'\
            '# ---------------------------------- WARNING ----------------------------------------\n'\
            '# Some of the data that you have obtained from this U.S. Geological Survey database\n'\
            '# may not have received Director\'s approval. Any such data values are qualified\n' \
            '# as provisional and are subject to revision. Provisional data are released on thev\n' \
            '# condition that neither the USGS nor the United States Government may be held liable\n' \
            '# for any damages resulting from its use.\n' \
            '#\n' \
            '# More data may be available offline.\n' \
            '# For more information on these data,  contact  USGS Water Data Inquiries.\n' \
            '# This file contains the annual peak streamflow data.\n'\
            '#\n' \
            '# This information includes the following fields:\n' \
            '#\n' \
            '#  agency_cd     Agency Code\n' \
            '#  site_no       USGS station number\n' \
            '#  peak_dt       Date of peak streamflow (format YYYY-MM-DD)\n' \
            '#  peak_tm       Time of peak streamflow (24 hour format, 00:00 - 23:59)\n' \
            '#  peak_va       Annual peak streamflow value in cfs\n' \
            '#  peak_cd       Peak Discharge-Qualification codes (see explanation below)\n' \
            '#  gage_ht       Gage height for the associated peak streamflow in feet\n' \
            '#  gage_ht_cd    Gage height qualification codes\n' \
            '#  year_last_pk  Peak streamflow reported is the highest since this year\n' \
            '#  ag_dt         Date of maximum gage-height for water year (if not concurrent with peak)\n' \
            '#  ag_tm         Time of maximum gage-height for water year (if not concurrent with peak\n' \
            '#  ag_gage_ht    maximum Gage height for water year in feet (if not concurrent with peak\n' \
            '#  ag_gage_ht_cd maximum Gage height code\n' \
            '#\n' \
            '# Sites in this file include:\n' \
            '#  USGS 05481950 Beaver Creek near Grimes, IA\n' \
            '#\n' \
            '# Peak Streamflow-Qualification Codes(peak_cd):\n' \
            '#   1 ... Discharge is a Maximum Daily Average\n' \
            '#   2 ... Discharge is an Estimate\n' \
            '#   3 ... Discharge affected by Dam Failure\n' \
            '#   4 ... Discharge less than indicated value,\n' \
            '#           which is Minimum Recordable Discharge at this site\n' \
            '#   5 ... Discharge affected to unknown degree by\n' \
            '#           Regulation or Diversion\n' \
            '#   6 ... Discharge affected by Regulation or Diversion\n' \
            '#   7 ... Discharge is an Historic Peak\n' \
            '#   8 ... Discharge actually greater than indicated value\n' \
            '#   9 ... Discharge due to Snowmelt, Hurricane,\n' \
            '#           Ice-Jam or Debris Dam breakup\n' \
            '#   A ... Year of occurrence is unknown or not exact\n' \
            '#   B ... Month or Day of occurrence is unknown or not exact\n' \
            '#   C ... All or part of the record affected by Urbanization,\n' \
            '#            Mining, Agricultural changes, Channelization, or other\n' \
            '#   D ... Base Discharge changed during this year\n' \
            '#   E ... Only Annual Maximum Peak available for this year\n' \
            '#\n' \
            '# Gage height qualification codes(gage_ht_cd,ag_gage_ht_cd):\n' \
            '#   1 ... Gage height affected by backwater\n' \
            '#   2 ... Gage height not the maximum for the year\n' \
            '#   3 ... Gage height at different site and(or) datum\n' \
            '#   4 ... Gage height below minimum recordable elevation\n' \
            '#   5 ... Gage height is an estimate\n' \
            '#   6 ... Gage datum changed during this year\n' \
            '#\n' \
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
            'USGS	05481950	1977-08-28		852		7.81						\n' \
            'USGS	05481950	1978-03-21		2980		11.38						\n' \
            'USGS	05481950	1979-03-20		4700		13.88						\n' \
            'USGS	05481950	1980-06-04		1730		9.02						\n' \
            'USGS	05481950	1981-08-14		1140		7.71						\n' \
            'USGS	05481950	1982-05-28		2780		11.32						\n' \
            'USGS	05481950	1983-06-29		3130		12.41						\n' \
            'USGS	05481950	1984-05-02		3220		11.76						\n' \
            'USGS	05481950	1984-12-28		1120		7.66						\n' \
            'USGS	05481950	1986-06-30		7980		14.73						\n' \
            'USGS	05481950	1987-08-28		2610		11.50						\n' \
            'USGS	05481950	1987-11-30		544		6.34	2		1988-02-01		6.91	1\n' \
            'USGS	05481950	1989-02-01		1540	2	11.35	1					\n' \
            'USGS	05481950	1990-06-19		5580		14.20						\n' \
            'USGS	05481950	1991-06-16		3340		11.96						\n' \
            'USGS	05481950	1992-04-23		1790		9.76						\n' \
            'USGS	05481950	1993-07-10		14300		16.58						\n' \
            'USGS	05481950	1994-03-06		1580		9.24						\n' \
            'USGS	05481950	1995-05-30		1960		10.12						\n' \
            'USGS	05481950	1996-05-10		1410		8.88						\n' \
            'USGS	05481950	1997-07-24		1920		9.97	2		1997-02-20		10.50	1\n' \
            'USGS	05481950	1998-06-17		4280		13.20						\n' \
            'USGS	05481950	1999-06-12		3820		12.36						\n' \
            'USGS	05481950	2000-07-05		533		6.36						\n' \
            'USGS	05481950	2001-03-17		2350		10.90						\n' \
            'USGS	05481950	2002-05-30		912		7.55	2		2002-05-13		7.70	\n' \
            'USGS	05481950	2003-05-06		3160		11.99						\n' \
            'USGS	05481950	2004-05-24		7300		14.59						\n' \
            'USGS	05481950	2005-05-14		2530		11.19						\n' \
            'USGS	05481950	2006-09-14	04:30	1740		9.47						\n' \
            'USGS	05481950	2007-04-27		6850		13.86						\n' \
            'USGS	05481950	2008-06-01		7800		14.51						'
        self.response_dv = '# ---------------------------------- WARNING ----------------------------------------\n'\
            '# Provisional data are subject to revision. Go to\n'\
            '# http://help.waterdata.usgs.gov/policies/provisional-data-statement for more information.\n'\
            '#\n'\
            '# File-format description:  http://help.waterdata.usgs.gov/faq/about-tab-delimited-output\n'\
            '# Automated-retrieval info: http://help.waterdata.usgs.gov/faq/automated-retrievals\n'\
            '#'\
            '# Contact:   gs-w_support_nwisweb@usgs.gov\n'\
            '# retrieved: 2017-07-03 14:46:35 -04:00 (natwebvaas01)\n'\
            '#\n'\
            '# Data for the following 1 site(s) are contained in this file\n'\
            '#    USGS 05481950 Beaver Creek near Grimes, IA\n'\
            '# -----------------------------------------------------------------------------------\n'\
            '#\n'\
            '# TS_ID - An internal number representing a time series.\n'\
            '# IV_TS_ID - An internal number representing the Instantaneous Value time series from which the daily'\
            'statistic is calculated.\n'\
            '#\n'\
            '# Data provided for site 05481950\n'\
            '#    TS_ID       Parameter    Statistic  IV_TS_ID       Description\n'\
            '#    43051       00060        00003      44227          Discharge, cubic feet per second (Mean)\n'\
            '#\n'\
            '# Data-value qualification codes included in this output:\n'\
            '#     A  Approved for publication -- Processing and review completed.\n'\
            '#\n'\
            'agency_cd\tsite_no\tdatetime\t43051_00060_00003\t43051_00060_00003_cd\n'\
            '5s      15s     20d     14n     10s\n'\
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


class TestMapUtilsRDBparse(unittest.TestCase):

    def setUp(self):
        self.mock_url = 'http://somethingfake.notadomain/noob/site/?format=rdb&sites=05420680,05463500&siteStatus=all'
        self.sites = ['05420680', '05463500']
        self.endpoint = 'https://waterservices.usgs.gov/nwis/'
        self.endpoint_mock = 'http://somethingfake.notadomain/noob/'
        self.header_values = {'site_no': 0,
                              'station_nm': 0,
                              'dec_long_va': 0,
                              'dec_lat_va': 0,
                              'huc_cd': 0
                              }
        self.test_dict = {
                 'sites': self.sites,
                 'site_query': '&sites=',
                 'site_status': '&siteStatus=all',
                 'format': '?format=rdb',
                 'extra': 'site/'
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

            # for item in data:
            #     self.assertIn(item, {})
