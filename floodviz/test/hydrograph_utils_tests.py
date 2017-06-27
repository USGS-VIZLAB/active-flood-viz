import unittest
import requests

class TestReqHydroData(unittest.TestCase):

  def setUp(self):
    self.prefix = 'https://waterservices.usgs.gov/nwis/'
    self.H_START_DT = '2008-05-20'
    self.H_END_DT = '2008-07-05'
    self.sites = ['05463500', '05471050', '05420680', '05479000', '05484000', '05481000', '05486000', '05421000', '05485500',
              '05455100', '05470500', '05451500', '05458000', '05471000', '05462000', '05457700', '05458500', '05470000',
              '05484500', '05481300', '05464220', '05458900', '05485605', '05463000', '05471200', '05476750', '05411850',
              '05454220', '05481950', '05416900', '05464500', '05487470']
   
  def test_empty_list(self):
    self.assertEqual(req_hydrodata([], self.H_START_DT, self.H_END_DT, self.prefix), [])

  def test_bad_list(self):
    self.assertEqual(req_hydrodata(['x'], self.H_START_DT, self.H_END_DT, self.prefix), [])
    self.assertEqual(req_hydrodata([123456, 100], self.H_START_DT, self.H_END_DT, self.prefix), [])

  def test_empty_url(self):
    self.assertEqual(req_hydrodata(self.sites, self.H_START_DT, self.H_END_DT, ''), [])

  def test_bad_url(self):
    self.assertEqual(req_hydrodata(self.sites, self.H_START_DT, self.H_END_DT, 'badurl.noob' ), [])

  def test_valid_data(self):
    self.assertTrue(req_hydrodata(self.sites, self.H_START_DT, self.H_END_DT, self.prefix))
 

class TestParseHydroData(unittest.TestCase):

  def setUp(self):

    self.mock_data = [{"sourceInfo": {
   "siteName": "Black Hawk Creek at Hudson, IA",
   "siteCode": [{"value": "05463500","network": "NWIS","agencyCode": "USGS"}],
   "timeZoneInfo": {"defaultTimeZone": {"zoneOffset": "-06:00","zoneAbbreviation": "CST"},"daylightSavingsTimeZone": {
    "zoneOffset": "-05:00","zoneAbbreviation": "CDT"},"siteUsesDaylightSavingsTime": True},"geoLocation": {
    "geogLocation": {"srs": "EPSG:4326","latitude": 42.4077639,"longitude": -92.4632451},"localSiteXY": []},
   "note": [],"siteType": [],},"variable": {"variableCode": [],"variableName": "Streamflow, ft&#179;/s",
   "variableDescription": "Discharge, cubic feet per second","valueType": "Derived Value","unit": {"unitCode": "ft3/s"},
   "note": [],},"values": [{"value": [{
      "value": "446","qualifiers": ["A"],"dateTime": "2008-05-20T00:00:00.000-05:00"},{
      "value": "446","qualifiers": ["A"],"dateTime": "2008-05-20T00:15:00.000-05:00"},{
      "value": "446","qualifiers": ["A"],"dateTime": "2008-05-20T00:30:00.000-05:00"},{
      "value": "444","qualifiers": ["A"],"dateTime": "2008-05-20T00:45:00.000-05:00"},{
      "value": "446","qualifiers": ["A"],"dateTime": "2008-05-20T01:00:00.000-05:00"},{
      "value": "446","qualifiers": ["A"],"dateTime": "2008-05-20T01:15:00.000-05:00"}]}]}]


  def test_data_is_none(self):
    self.assertEqual(parse_hydrodata(None), [])

  def test_empty_data(self):
    self.assertEqual(parse_hydrodata([]), [])

  def test_data_not_list(self):
    self.assertEqual(parse_hydrodata("Not a REAL list"), [])
    self.assertEqual(parse_hydrodata({}), [])

  def invalid_elements(self):
    self.assertEqual(parse_hydrodata([{} ,'A', 'B']), [])

  def test_valid_data(self):
    self.assertTrue(parse_hydrodata(self.mock_data))



if __name__ == '__main__':
 
  if __package__ is None:
      import sys
      from os import path
      sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
      from hydrograph_utils import req_hydrodata, parse_hydrodata
  else:
      from ..floodviz.hydrograph_utils import req_hydrodata, parse_hydrodata

  unittest.main()