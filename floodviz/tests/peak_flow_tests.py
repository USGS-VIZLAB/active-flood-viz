import unittest
import requests_mock
from floodviz.peak_flow_utils import req_peak_data, req_peak_dv_data, parse_peak_data

class BaseTestCase(unittest.TestCase):
  return_peak = ['#', '# U.S. Geological Survey', '# National Water Information System', '# Retrieved: 2017-07-03 15:51:52 EDT', '#', '# ---------------------------------- WARNING ----------------------------------------', '# Some of the data that you have obtained from this U.S. Geological Survey database', "# may not have received Director's approval. Any such data values are qualified", '# as provisional and are subject to revision. Provisional data are released on the', '# condition that neither the USGS nor the United States Government may be held liable', '# for any damages resulting from its use.', '#', '# More data may be available offline.', '# For more information on these data,  contact  USGS Water Data Inquiries.', '# This file contains the annual peak streamflow data.', '#', '# This information includes the following fields:', '#', '#  agency_cd     Agency Code', '#  site_no       USGS station number', '#  peak_dt       Date of peak streamflow (format YYYY-MM-DD)', '#  peak_tm       Time of peak streamflow (24 hour format, 00:00 - 23:59)', '#  peak_va       Annual peak streamflow value in cfs', '#  peak_cd       Peak Discharge-Qualification codes (see explanation below)', '#  gage_ht       Gage height for the associated peak streamflow in feet', '#  gage_ht_cd    Gage height qualification codes', '#  year_last_pk  Peak streamflow reported is the highest since this year', '#  ag_dt         Date of maximum gage-height for water year (if not concurrent with peak)', '#  ag_tm         Time of maximum gage-height for water year (if not concurrent with peak', '#  ag_gage_ht    maximum Gage height for water year in feet (if not concurrent with peak', '#  ag_gage_ht_cd maximum Gage height code', '#', '# Sites in this file include:', '#  USGS 05481950 Beaver Creek near Grimes, IA', '#', '# Peak Streamflow-Qualification Codes(peak_cd):', '#   1 ... Discharge is a Maximum Daily Average', '#   2 ... Discharge is an Estimate', '#   3 ... Discharge affected by Dam Failure', '#   4 ... Discharge less than indicated value,', '#           which is Minimum Recordable Discharge at this site', '#   5 ... Discharge affected to unknown degree by', '#           Regulation or Diversion', '#   6 ... Discharge affected by Regulation or Diversion', '#   7 ... Discharge is an Historic Peak', '#   8 ... Discharge actually greater than indicated value', '#   9 ... Discharge due to Snowmelt, Hurricane,', '#           Ice-Jam or Debris Dam breakup', '#   A ... Year of occurrence is unknown or not exact', '#   B ... Month or Day of occurrence is unknown or not exact', '#   C ... All or part of the record affected by Urbanization,', '#            Mining, Agricultural changes, Channelization, or other', '#   D ... Base Discharge changed during this year', '#   E ... Only Annual Maximum Peak available for this year', '#', '# Gage height qualification codes(gage_ht_cd,ag_gage_ht_cd):', '#   1 ... Gage height affected by backwater', '#   2 ... Gage height not the maximum for the year', '#   3 ... Gage height at different site and(or) datum', '#   4 ... Gage height below minimum recordable elevation', '#   5 ... Gage height is an estimate', '#   6 ... Gage datum changed during this year', '#', '#', 'agency_cd\tsite_no\tpeak_dt\tpeak_tm\tpeak_va\tpeak_cd\tgage_ht\tgage_ht_cd\tyear_last_pk\tag_dt\tag_tm\tag_gage_ht\tag_gage_ht_cd', '5s\t15s\t10d\t6s\t8s\t27s\t8s\t13s\t4s\t10d\t6s\t8s\t11s', 'USGS\t05481950\t1960-05-26\t\t5480\t\t14.05\t\t\t\t\t\t', 'USGS\t05481950\t1961-06-08\t\t1870\t\t11.05\t\t\t\t\t\t', 'USGS\t05481950\t1962-05-30\t\t3780\t\t12.90\t\t\t\t\t\t', 'USGS\t05481950\t1963-08-07\t\t2540\t\t11.80\t\t\t\t\t\t', 'USGS\t05481950\t1964-05-10\t\t2010\t\t11.25\t2\t\t1964-06-23\t\t11.70\t', 'USGS\t05481950\t1965-04-02\t\t4230\t\t13.25\t\t\t\t\t\t', 'USGS\t05481950\t1966-06-13\t\t5470\t\t14.04\t\t\t\t\t\t', 'USGS\t05481950\t1967-06-10\t\t4000\t\t13.11\t\t\t\t\t\t', 'USGS\t05481950\t1968-06-28\t\t2000\t\t11.24\t\t\t\t\t\t', 'USGS\t05481950\t1969-03-19\t\t4050\t\t13.04\t\t\t\t\t\t', 'USGS\t05481950\t1970-05-15\t\t3810\t\t12.97\t\t\t\t\t\t', 'USGS\t05481950\t1971-02-20\t\t1900\t2\t13.35\t1\t\t\t\t\t', 'USGS\t05481950\t1972-08-04\t\t1080\t\t8.70\t\t\t\t\t\t', 'USGS\t05481950\t1973-04-17\t\t4130\t\t12.94\t\t\t\t\t\t', 'USGS\t05481950\t1974-05-19\t\t7340\t\t14.69\t\t\t\t\t\t', 'USGS\t05481950\t1975-03-18\t\t2500\t2\t11.61\t1\t\t\t\t\t', 'USGS\t05481950\t1976-04-18\t\t1960\t\t9.62\t\t\t\t\t\t', 'USGS\t05481950\t1977-08-28\t\t852\t\t7.81\t\t\t\t\t\t', 'USGS\t05481950\t1978-03-21\t\t2980\t\t11.38\t\t\t\t\t\t', 'USGS\t05481950\t1979-03-20\t\t4700\t\t13.88\t\t\t\t\t\t', 'USGS\t05481950\t1980-06-04\t\t1730\t\t9.02\t\t\t\t\t\t', 'USGS\t05481950\t1981-08-14\t\t1140\t\t7.71\t\t\t\t\t\t', 'USGS\t05481950\t1982-05-28\t\t2780\t\t11.32\t\t\t\t\t\t', 'USGS\t05481950\t1983-06-29\t\t3130\t\t12.41\t\t\t\t\t\t', 'USGS\t05481950\t1984-05-02\t\t3220\t\t11.76\t\t\t\t\t\t', 'USGS\t05481950\t1984-12-28\t\t1120\t\t7.66\t\t\t\t\t\t', 'USGS\t05481950\t1986-06-30\t\t7980\t\t14.73\t\t\t\t\t\t', 'USGS\t05481950\t1987-08-28\t\t2610\t\t11.50\t\t\t\t\t\t', 'USGS\t05481950\t1987-11-30\t\t544\t\t6.34\t2\t\t1988-02-01\t\t6.91\t1', 'USGS\t05481950\t1989-02-01\t\t1540\t2\t11.35\t1\t\t\t\t\t', 'USGS\t05481950\t1990-06-19\t\t5580\t\t14.20\t\t\t\t\t\t', 'USGS\t05481950\t1991-06-16\t\t3340\t\t11.96\t\t\t\t\t\t', 'USGS\t05481950\t1992-04-23\t\t1790\t\t9.76\t\t\t\t\t\t', 'USGS\t05481950\t1993-07-10\t\t14300\t\t16.58\t\t\t\t\t\t', 'USGS\t05481950\t1994-03-06\t\t1580\t\t9.24\t\t\t\t\t\t', 'USGS\t05481950\t1995-05-30\t\t1960\t\t10.12\t\t\t\t\t\t', 'USGS\t05481950\t1996-05-10\t\t1410\t\t8.88\t\t\t\t\t\t', 'USGS\t05481950\t1997-07-24\t\t1920\t\t9.97\t2\t\t1997-02-20\t\t10.50\t1', 'USGS\t05481950\t1998-06-17\t\t4280\t\t13.20\t\t\t\t\t\t', 'USGS\t05481950\t1999-06-12\t\t3820\t\t12.36\t\t\t\t\t\t', 'USGS\t05481950\t2000-07-05\t\t533\t\t6.36\t\t\t\t\t\t', 'USGS\t05481950\t2001-03-17\t\t2350\t\t10.90\t\t\t\t\t\t', 'USGS\t05481950\t2002-05-30\t\t912\t\t7.55\t2\t\t2002-05-13\t\t7.70\t', 'USGS\t05481950\t2003-05-06\t\t3160\t\t11.99\t\t\t\t\t\t', 'USGS\t05481950\t2004-05-24\t\t7300\t\t14.59\t\t\t\t\t\t', 'USGS\t05481950\t2005-05-14\t\t2530\t\t11.19\t\t\t\t\t\t', 'USGS\t05481950\t2006-09-14\t04:30\t1740\t\t9.47\t\t\t\t\t\t', 'USGS\t05481950\t2007-04-27\t\t6850\t\t13.86\t\t\t\t\t\t', 'USGS\t05481950\t2008-06-01\t\t7800\t\t14.51\t\t\t\t\t\t']
  return_dv = ['# ---------------------------------- WARNING ----------------------------------------', '# Provisional data are subject to revision. Go to', '# http://help.waterdata.usgs.gov/policies/provisional-data-statement for more information.', '#', '# File-format description:  http://help.waterdata.usgs.gov/faq/about-tab-delimited-output', '# Automated-retrieval info: http://help.waterdata.usgs.gov/faq/automated-retrievals', '#', '# Contact:   gs-w_support_nwisweb@usgs.gov', '# retrieved: 2017-07-03 15:51:52 -04:00\t(natwebvaas01)', '#', '# Data for the following 1 site(s) are contained in this file', '#    USGS 05481950 Beaver Creek near Grimes, IA', '# -----------------------------------------------------------------------------------', '#', '# TS_ID - An internal number representing a time series.', '# IV_TS_ID - An internal number representing the Instantaneous Value time series from which the daily statistic is calculated.', '#', '# Data provided for site 05481950', '#    TS_ID       Parameter    Statistic  IV_TS_ID       Description', '#    43051       00060        00003      44227          Discharge, cubic feet per second (Mean)', '#', '# Data-value qualification codes included in this output:', '#     A  Approved for publication -- Processing and review completed.', '#', 'agency_cd\tsite_no\tdatetime\t43051_00060_00003\t43051_00060_00003_cd', '5s\t15s\t20d\t14n\t10s', 'USGS\t05481950\t2008-07-05\t430\tA']
  mock_response_peak = '# \
        # U.S. Geological Survey\
        # National Water Information System\
        # Retrieved: 2017-07-03 14:37:04 EDT\
        #\
        # ---------------------------------- WARNING ----------------------------------------\
        # Some of the data that you have obtained from this U.S. Geological Survey database\
        # may not have received Director\'s approval. Any such data values are qualified\
        # as provisional and are subject to revision. Provisional data are released on the\
        # condition that neither the USGS nor the United States Government may be held liable\
        # for any damages resulting from its use.\
        #\
        # More data may be available offline.\
        # For more information on these data,  contact  USGS Water Data Inquiries.\
        # This file contains the annual peak streamflow data.\
        #\
        # This information includes the following fields:\
        #\
        #  agency_cd     Agency Code\
        #  site_no       USGS station number\
        #  peak_dt       Date of peak streamflow (format YYYY-MM-DD)\
        #  peak_tm       Time of peak streamflow (24 hour format, 00:00 - 23:59)\
        #  peak_va       Annual peak streamflow value in cfs\
        #  peak_cd       Peak Discharge-Qualification codes (see explanation below)\
        #  gage_ht       Gage height for the associated peak streamflow in feet\
        #  gage_ht_cd    Gage height qualification codes\
        #  year_last_pk  Peak streamflow reported is the highest since this year\
        #  ag_dt         Date of maximum gage-height for water year (if not concurrent with peak)\
        #  ag_tm         Time of maximum gage-height for water year (if not concurrent with peak\
        #  ag_gage_ht    maximum Gage height for water year in feet (if not concurrent with peak\
        #  ag_gage_ht_cd maximum Gage height code\
        #\
        # Sites in this file include:\
        #  USGS 05481950 Beaver Creek near Grimes, IA\
        #\
        # Peak Streamflow-Qualification Codes(peak_cd):\
        #   1 ... Discharge is a Maximum Daily Average\
        #   2 ... Discharge is an Estimate\
        #   3 ... Discharge affected by Dam Failure\
        #   4 ... Discharge less than indicated value,\
        #           which is Minimum Recordable Discharge at this site\
        #   5 ... Discharge affected to unknown degree by\
        #           Regulation or Diversion\
        #   6 ... Discharge affected by Regulation or Diversion\
        #   7 ... Discharge is an Historic Peak\
        #   8 ... Discharge actually greater than indicated value\
        #   9 ... Discharge due to Snowmelt, Hurricane,\
        #           Ice-Jam or Debris Dam breakup\
        #   A ... Year of occurrence is unknown or not exact\
        #   B ... Month or Day of occurrence is unknown or not exact\
        #   C ... All or part of the record affected by Urbanization,\
        #            Mining, Agricultural changes, Channelization, or other\
        #   D ... Base Discharge changed during this year\
        #   E ... Only Annual Maximum Peak available for this year\
        #\
        # Gage height qualification codes(gage_ht_cd,ag_gage_ht_cd):\
        #   1 ... Gage height affected by backwater\
        #   2 ... Gage height not the maximum for the year\
        #   3 ... Gage height at different site and(or) datum\
        #   4 ... Gage height below minimum recordable elevation\
        #   5 ... Gage height is an estimate\
        #   6 ... Gage datum changed during this year\
        #\
        #\
        agency_cd       site_no peak_dt peak_tm peak_va peak_cd gage_ht gage_ht_cd      year_last_pk    ag_dt   ag_tm   ag_gage_ht      ag_gage_ht_cd\
        5s      15s     10d     6s      8s      27s     8s      13s     4s      10d     6s      8s      11s\
        USGS    05481950        1960-05-26              5480            14.05\
        USGS    05481950        1961-06-08              1870            11.05\
        USGS    05481950        1962-05-30              3780            12.90\
        USGS    05481950        1963-08-07              2540            11.80\
        USGS    05481950        1964-05-10              2010            11.25   2               1964-06-23      11.70\
        USGS    05481950        1965-04-02              4230            13.25\
        USGS    05481950        1966-06-13              5470            14.04\
        USGS    05481950        1967-06-10              4000            13.11\
        USGS    05481950        1968-06-28              2000            11.24\
        USGS    05481950        1969-03-19              4050            13.04\
        USGS    05481950        1970-05-15              3810            12.97\
        USGS    05481950        1971-02-20              1900    2       13.35   1\
        USGS    05481950        1972-08-04              1080            8.70\
        USGS    05481950        1973-04-17              4130            12.94\
        USGS    05481950        1974-05-19              7340            14.69\
        USGS    05481950        1975-03-18              2500    2       11.61   1\
        USGS    05481950        1976-04-18              1960            9.62\
        USGS    05481950        1977-08-28              852             7.81\
        USGS    05481950        1978-03-21              2980            11.38\
        USGS    05481950        1979-03-20              4700            13.88\
        USGS    05481950        1980-06-04              1730            9.02\
        USGS    05481950        1981-08-14              1140            7.71\
        USGS    05481950        1982-05-28              2780            11.32\
        USGS    05481950        1983-06-29              3130            12.41\
        USGS    05481950        1984-05-02              3220            11.76\
        USGS    05481950        1984-12-28              1120            7.66\
        USGS    05481950        1986-06-30              7980            14.73\
        USGS    05481950        1987-08-28              2610            11.50\
        USGS    05481950        1987-11-30              544             6.34    2               1988-02-01      6.91    1\
        USGS    05481950        1989-02-01              1540    2       11.35   1\
        USGS    05481950        1990-06-19              5580            14.20\
        USGS    05481950        1991-06-16              3340            11.96\
        USGS    05481950        1992-04-23              1790            9.76\
        USGS    05481950        1993-07-10              14300           16.58\
        USGS    05481950        1994-03-06              1580            9.24\
        USGS    05481950        1995-05-30              1960            10.12\
        USGS    05481950        1996-05-10              1410            8.88\
        USGS    05481950        1997-07-24              1920            9.97    2               1997-02-20      10.50   1\
        USGS    05481950        1998-06-17              4280            13.20\
        USGS    05481950        1999-06-12              3820            12.36\
        USGS    05481950        2000-07-05              533             6.36\
        USGS    05481950        2001-03-17              2350            10.90\
        USGS    05481950        2002-05-30              912             7.55    2               2002-05-13      7.70\
        USGS    05481950        2003-05-06              3160            11.99\
        USGS    05481950        2004-05-24              7300            14.59\
        USGS    05481950        2005-05-14              2530            11.19\
        USGS    05481950        2006-09-14      04:30   1740            9.47\
        USGS    05481950        2007-04-27              6850            13.86\
        USGS    05481950        2008-06-01              7800            14.51'
  mock_response_dv = '# ---------------------------------- WARNING ----------------------------------------\
        # Provisional data are subject to revision. Go to\
        # http://help.waterdata.usgs.gov/policies/provisional-data-statement for more information.\
        #\
        # File-format description:  http://help.waterdata.usgs.gov/faq/about-tab-delimited-output\
        # Automated-retrieval info: http://help.waterdata.usgs.gov/faq/automated-retrievals\
        #\
        # Contact:   gs-w_support_nwisweb@usgs.gov\
        # retrieved: 2017-07-03 14:46:35 -04:00 (natwebvaas01)\
        #\
        # Data for the following 1 site(s) are contained in this file\
        #    USGS 05481950 Beaver Creek near Grimes, IA\
        # -----------------------------------------------------------------------------------\
        #\
        # TS_ID - An internal number representing a time series.\
        # IV_TS_ID - An internal number representing the Instantaneous Value time series from which the daily statistic is calculated.\
        #\
        # Data provided for site 05481950\
        #    TS_ID       Parameter    Statistic  IV_TS_ID       Description\
        #    43051       00060        00003      44227          Discharge, cubic feet per second (Mean)\
        #\
        # Data-value qualification codes included in this output:\
        #     A  Approved for publication -- Processing and review completed.\
        #\
        agency_cd       site_no datetime        43051_00060_00003       43051_00060_00003_cd\
        5s      15s     20d     14n     10s\
        USGS    05481950        2008-07-05      430     A'

class TestReqPeakData(BaseTestCase):

  def setUp(self):

    ## Returned value is different than the mocked request response because req_hydrodata accessess two extra levels of the dict before returning.
    
    self.prefix = 'http://somethingfake.notadomain/peak'
    self.P_START_DT = '2008-05-20'
    self.P_END_DT = '2008-07-05'
    self.site = '05481950'
    self.mock_url = self.prefix + '?site_no=' + self.site + '&agency_cd=USGS&format=rdb&end_date=' + self.P_END_DT 

  def test_bad_status_code(self):
    with requests_mock.Mocker() as m:
      m.get(self.mock_url, status_code=404)
      self.assertEqual(req_peak_data(self.site, self.P_START_DT, self.P_END_DT, self.prefix), None)

  def test_valid_data(self):
    with requests_mock.Mocker() as m:
      m.get(self.mock_url, text=self.mock_response_peak)
      self.assertEqual(req_peak_data(self.site, self.P_START_DT, self.P_END_DT, self.prefix), [self.mock_response_peak])

  def test_bad_site(self):
    self.assertEqual(req_peak_data('x', self.P_START_DT, self.P_END_DT, self.prefix), None)
    self.assertEqual(req_peak_data('', self.P_START_DT, self.P_END_DT, self.prefix), None)

  def test_bad_url(self):
    self.assertEqual(req_peak_data(self.site, self.P_START_DT, self.P_END_DT, 'badurl.noob' ), None)
    self.assertEqual(req_peak_data(self.site, self.P_START_DT, self.P_END_DT, ''), None)
 

class TestReqPeakDVData(BaseTestCase):

  def setUp(self):

    self.prefix = 'http://somethingfake.notadomain/'
    self.date = '2008-07-05'
    self.site = '05481950'
    self.mock_url = self.prefix + 'dv/?format=rdb&sites=' + self.site + '&startDT=' + self.date + '&endDT=' + self.date + '&siteStatus=all'

  def test_bad_status_code(self):
    with requests_mock.Mocker() as m:
      m.get(self.mock_url, status_code=404)
      self.assertEqual(req_peak_dv_data(self.site, self.date, self.prefix), None)

  def test_valid_data(self):
    with requests_mock.Mocker() as m:
      m.get(self.mock_url, text=self.mock_response_dv)
      self.assertEqual(req_peak_dv_data(self.site, self.date, self.prefix), [self.mock_response_dv])

  def test_bad_site(self):
    self.assertEqual(req_peak_dv_data('x', self.date, self.prefix), None)
    self.assertEqual(req_peak_dv_data('', self.date, self.prefix), None)

  def test_bad_url(self):
    self.assertEqual(req_peak_dv_data(self.site, self.date, 'badurl.noob' ), None)
    self.assertEqual(req_peak_dv_data(self.site, self.date, ''), None)


class TestParsePeakData(BaseTestCase):

  def setUp(self):

    self.mock_peak_in = self.return_peak
    self.mock_dv_in = self.return_dv

    self.valid_parsed = [{'label': '1960', 'value': 5480}, {'label': '1961', 'value': 1870}, {'label': '1962', 'value': 3780}, {'label': '1963', 'value': 2540},
    {'label': '1964', 'value': 2010}, {'label': '1965', 'value': 4230}, {'label': '1966', 'value': 5470}, {'label': '1967', 'value': 4000}, {'label': '1968', 'value': 2000}, 
    {'label': '1969', 'value': 4050}, {'label': '1970', 'value': 3810}, {'label': '1971', 'value': 1900}, {'label': '1972', 'value': 1080}, {'label': '1973', 'value': 4130}, 
    {'label': '1974', 'value': 7340}, {'label': '1975', 'value': 2500}, {'label': '1976', 'value': 1960}, {'label': '1977', 'value': 852}, {'label': '1978', 'value': 2980}, 
    {'label': '1979', 'value': 4700}, {'label': '1980', 'value': 1730}, {'label': '1981', 'value': 1140}, {'label': '1982', 'value': 2780}, {'label': '1983', 'value': 3130}, 
    {'label': '1984', 'value': 3220}, {'label': '1986', 'value': 7980}, {'label': '1987', 'value': 2610}, {'label': '1989', 'value': 1540}, {'label': '1990', 'value': 5580}, 
    {'label': '1991', 'value': 3340}, {'label': '1992', 'value': 1790}, {'label': '1993', 'value': 14300}, {'label': '1994', 'value': 1580}, {'label': '1995', 'value': 1960}, 
    {'label': '1996', 'value': 1410}, {'label': '1997', 'value': 1920}, {'label': '1998', 'value': 4280}, {'label': '1999', 'value': 3820}, {'label': '2000', 'value': 533}, 
    {'label': '2001', 'value': 2350}, {'label': '2002', 'value': 912}, {'label': '2003', 'value': 3160}, {'label': '2004', 'value': 7300}, {'label': '2005', 'value': 2530}, 
    {'label': '2006', 'value': 1740}, {'label': '2007', 'value': 6850}, {'label': '2008', 'value': 7800}]

  def test_empty_data(self):
    self.assertEqual(parse_peak_data([], []), [])

  def test_data_not_list(self):
    self.assertEqual(parse_peak_data({}, {}), [])
    self.assertEqual(parse_peak_data(None, None), [])

  def test_valid_data(self):
    self.assertEqual(parse_peak_data(self.mock_peak_in, self.mock_dv_in), self.valid_parsed)