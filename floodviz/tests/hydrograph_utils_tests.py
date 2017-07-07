import unittest
import requests_mock
from floodviz.hydrograph_utils import req_hydrodata, parse_hydrodata

class TestReqHydroData(unittest.TestCase):

    def setUp(self):

        self.mock_response = {"value": {"timeSeries": {"sourceInfo": {"siteName": "Black Hawk Creek at Hudson, IA", "siteCode":
            [{"value": "05463500", "network": "NWIS", "agencyCode": "USGS"}], "timeZoneInfo": {"defaultTimeZone":
                                                                                                   {"zoneOffset": "-06:00", "zoneAbbreviation": "CST"}, "daylightSavingsTimeZone": {"zoneOffset": "-05:00", "zoneAbbreviation": "CDT"},
                                                                                               "siteUsesDaylightSavingsTime": True}, "geoLocation": {"geogLocation": {"srs": "EPSG:4326", "latitude": 42.4077639, "longitude": -92.4632451},
                                                                                                                                                     "localSiteXY": []}, "note": [], "siteType": [], "siteProperty": [{"value": "ST", "name": "siteTypeCd"}, {"value": "07080205", "name": "hucCd"},
                                                                                                                                                                                                                      {"value": "19", "name": "stateCd"}, {"value": "19013", "name": "countyCd"}]}, "variable": {"variableCode": [{"value": "00060", "network": "NWIS",
                                                                                                                                                                                                                                                                                                                                   "vocabulary": "NWIS:UnitValues", "variableID": 45807197, "default": True}], "variableName": "Streamflow, ft&#179;/s", "variableDescription":
                                                                                                                                                                                                                                                                                                                     "Discharge, cubic feet per second", "valueType": "Derived Value", "unit": {"unitCode": "ft3/s"}, "options": {"option":
                                                                                                                                                                                                                                                                                                                                                                                                                                      [{"name": "Statistic", "optionCode": "00000"}]}, "note": [], "noDataValue": -999999.0, "variableProperty": [], "oid": "45807197"}, "values":
                                                           [{"value": [{"value": "446", "qualifiers": ["A"], "dateTime": "2008-05-20T00:00:00.000-05:00"}]}]}}}

        ## Returned value is different than the mocked request response because req_hydrodata accessess two extra levels of the dict before returning.
        self.valid_return = {"sourceInfo": {"siteName": "Black Hawk Creek at Hudson, IA", "siteCode":
            [{"value": "05463500", "network": "NWIS", "agencyCode": "USGS"}], "timeZoneInfo": {"defaultTimeZone":
                                                                                                   {"zoneOffset": "-06:00", "zoneAbbreviation": "CST"}, "daylightSavingsTimeZone": {"zoneOffset": "-05:00", "zoneAbbreviation": "CDT"},
                                                                                               "siteUsesDaylightSavingsTime": True}, "geoLocation": {"geogLocation": {"srs": "EPSG:4326", "latitude": 42.4077639, "longitude": -92.4632451},
                                                                                                                                                     "localSiteXY": []}, "note": [], "siteType": [], "siteProperty": [{"value": "ST", "name": "siteTypeCd"}, {"value": "07080205", "name": "hucCd"},
                                                                                                                                                                                                                      {"value": "19", "name": "stateCd"}, {"value": "19013", "name": "countyCd"}]}, "variable": {"variableCode": [{"value": "00060", "network": "NWIS",
                                                                                                                                                                                                                                                                                                                                   "vocabulary": "NWIS:UnitValues", "variableID": 45807197, "default": True}], "variableName": "Streamflow, ft&#179;/s", "variableDescription":
                                                                                                                                                                                                                                                                                                                     "Discharge, cubic feet per second", "valueType": "Derived Value", "unit": {"unitCode": "ft3/s"}, "options": {"option":
                                                                                                                                                                                                                                                                                                                                                                                                                                      [{"name": "Statistic", "optionCode": "00000"}]}, "note": [], "noDataValue": -999999.0, "variableProperty": [], "oid": "45807197"}, "values":
                                 [{"value": [{"value": "446", "qualifiers": ["A"], "dateTime": "2008-05-20T00:00:00.000-05:00"}]}]}

        self.mock_url = 'http://somethingfake.notadomain/iv/?site=05463500&startDT=2008-05-20&endDT=2008-07-05&parameterCD=00060&format=json'
        self.prefix = 'http://somethingfake.notadomain/'
        self.H_START_DT = '2008-05-20'
        self.H_END_DT = '2008-07-05'
        self.sites = ['05463500', '05471050', '05420680', '05479000', '05484000', '05481000', '05486000', '05421000', '05485500',
                      '05455100', '05470500', '05451500', '05458000', '05471000', '05462000', '05457700', '05458500', '05470000',
                      '05484500', '05481300', '05464220', '05458900', '05485605', '05463000', '05471200', '05476750', '05411850',
                      '05454220', '05481950', '05416900', '05464500', '05487470']

    def test_bad_status_code(self):
        with requests_mock.Mocker() as m:
            m.get(self.mock_url, status_code=404)
            self.assertEqual(req_hydrodata(['05463500'], self.H_START_DT, self.H_END_DT, self.prefix), None)

    def test_valid_data(self):
        with requests_mock.Mocker() as m:
            m.get(self.mock_url, json=self.mock_response)
            self.assertEqual(req_hydrodata(['05463500'], self.H_START_DT, self.H_END_DT, self.prefix), self.valid_return)

    def test_bad_list(self):
        self.assertEqual(req_hydrodata(['x'], self.H_START_DT, self.H_END_DT, self.prefix), None)
        self.assertEqual(req_hydrodata([123456, 100], self.H_START_DT, self.H_END_DT, self.prefix), None)
        self.assertEqual(req_hydrodata([], self.H_START_DT, self.H_END_DT, self.prefix), None)

    def test_bad_url(self):
        self.assertEqual(req_hydrodata(self.sites, self.H_START_DT, self.H_END_DT, 'badurl.noob' ), None)
        self.assertEqual(req_hydrodata(self.sites, self.H_START_DT, self.H_END_DT, ''), None)


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
            "value": "446","qualifiers": ["A"],"dateTime": "2008-05-20T00:30:00.000-05:00"}]}]}]

        self.mock_parsed_data = [{
            "key": "05463500",
            "name": "Black Hawk Creek at Hudson, IA",
            "date": "2008-05-20",
            "time": "00:00:00",
            "time_mili": 1211259600000.0,
            "value": "446"
        },
            {
                "key": "05463500",
                "name": "Black Hawk Creek at Hudson, IA",
                "date": "2008-05-20",
                "time": "00:15:00",
                "time_mili": 1211260500000.0,
                "value": "446"
            },
            {
                "key": "05463500",
                "name": "Black Hawk Creek at Hudson, IA",
                "date": "2008-05-20",
                "time": "00:30:00",
                "time_mili": 1211261400000.0,
                "value": "446"
            }]


    def test_empty_data(self):
        self.assertEqual(parse_hydrodata([]), [])
        self.assertEqual(parse_hydrodata(None), [])

    def test_data_not_list(self):
        self.assertEqual(parse_hydrodata({}), [])

    def test_valid_data(self):
        def test_valid_data(self):
            # Delete 'time_mili' key before comparing due to python time conversion inconsistencies.
            ret = parse_hydrodata(self.mock_data)[0]
            for k1, v1 in ret.items():
                if k1 is 'values':
                    for item in ret[k1]:
                        if item['time_mili'] is not None:
                            del item['time_mili']
            self.assertEqual([ret], self.mock_parsed_data)
