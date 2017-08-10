import unittest
import requests_mock
import time
from datetime import datetime
from floodviz.hydrograph_utils import req_hydrodata, parse_hydrodata


class TestReqHydroData(unittest.TestCase):
    def setUp(self):
        self.mock_response = {
            "value": {"timeSeries": {"sourceInfo": {"siteName": "Black Hawk Creek at Hudson, IA", "siteCode":
                [{"value": "05463500", "network": "NWIS", "agencyCode": "USGS"}], "timeZoneInfo": {"defaultTimeZone":
                                                                                                       {
                                                                                                           "zoneOffset": "-06:00",
                                                                                                           "zoneAbbreviation": "CST"},
                                                                                                   "daylightSavingsTimeZone": {
                                                                                                       "zoneOffset": "-05:00",
                                                                                                       "zoneAbbreviation": "CDT"},
                                                                                                   "siteUsesDaylightSavingsTime": True},
                                                    "geoLocation": {
                                                        "geogLocation": {"srs": "EPSG:4326", "latitude": 42.4077639,
                                                                         "longitude": -92.4632451},
                                                        "localSiteXY": []}, "note": [], "siteType": [],
                                                    "siteProperty": [{"value": "ST", "name": "siteTypeCd"},
                                                                     {"value": "07080205", "name": "hucCd"},
                                                                     {"value": "19", "name": "stateCd"},
                                                                     {"value": "19013", "name": "countyCd"}]},
                                     "variable": {"variableCode": [{"value": "00060", "network": "NWIS",
                                                                    "vocabulary": "NWIS:UnitValues",
                                                                    "variableID": 45807197, "default": True}],
                                                  "variableName": "Streamflow, ft&#179;/s", "variableDescription":
                                                      "Discharge, cubic feet per second", "valueType": "Derived Value",
                                                  "unit": {"unitCode": "ft3/s"},
                                                  "options": {"option": [{"name": "Statistic", "optionCode": "00000"}]},
                                                  "note": [], "noDataValue": -999999.0, "variableProperty": [],
                                                  "oid": "45807197"}, "values":
                                         [{"value": [{"value": "446", "qualifiers": ["A"],
                                                      "dateTime": "2008-05-20T00:00:00.000-05:00"}]}]}}}

        # Returned value is different than the mocked request response because req_hydrodata accessess two extra
        # levels of the dict before returning.
        self.valid_return = {"sourceInfo": {"siteName": "Black Hawk Creek at Hudson, IA", "siteCode":
            [{"value": "05463500", "network": "NWIS", "agencyCode": "USGS"}], "timeZoneInfo": {"defaultTimeZone":
                                                                                                   {
                                                                                                       "zoneOffset": "-06:00",
                                                                                                       "zoneAbbreviation": "CST"},
                                                                                               "daylightSavingsTimeZone": {
                                                                                                   "zoneOffset": "-05:00",
                                                                                                   "zoneAbbreviation": "CDT"},
                                                                                               "siteUsesDaylightSavingsTime": True},
                                            "geoLocation": {"geogLocation": {"srs": "EPSG:4326", "latitude": 42.4077639,
                                                                             "longitude": -92.4632451},
                                                            "localSiteXY": []}, "note": [], "siteType": [],
                                            "siteProperty": [{"value": "ST", "name": "siteTypeCd"},
                                                             {"value": "07080205", "name": "hucCd"},
                                                             {"value": "19", "name": "stateCd"},
                                                             {"value": "19013", "name": "countyCd"}]},
                             "variable": {"variableCode": [{"value": "00060", "network": "NWIS",
                                                            "vocabulary": "NWIS:UnitValues", "variableID": 45807197,
                                                            "default": True}], "variableName": "Streamflow, ft&#179;/s",
                                          "variableDescription": "Discharge, cubic feet per second",
                                          "valueType": "Derived Value",
                                          "unit": {"unitCode": "ft3/s"}, "options": {"option": [{"name": "Statistic",
                                                                                                 "optionCode": "00000"}]},
                                          "note": [], "noDataValue": -999999.0, "variableProperty": [],
                                          "oid": "45807197"},
                             "values": [{"value": [{"value": "446", "qualifiers": ["A"],
                                                    "dateTime": "2008-05-20T00:00:00.000-05:00"}]}]}

        self.mock_url = 'http://somethingfake.notadomain/iv/?site=05463500&startDT=2008-05-20&endDT=2008-07-05&parameterCD=00060&format=json'
        self.prefix = 'http://somethingfake.notadomain/'
        self.H_START_DT = '2008-05-20'
        self.H_END_DT = '2008-07-05'
        self.sites = ['05463500', '05471050', '05420680', '05479000', '05484000', '05481000', '05486000', '05421000',
                      '05485500', '05455100', '05470500', '05451500', '05458000', '05471000', '05462000', '05457700',
                      '05458500', '05470000', '05484500', '05481300', '05464220', '05458900', '05485605', '05463000',
                      '05471200', '05476750', '05411850', '05454220', '05481950', '05416900', '05464500', '05487470']

    def test_bad_status_code(self):
        with requests_mock.Mocker() as m:
            m.get(self.mock_url, status_code=404)
            self.assertEqual(req_hydrodata(['05463500'], self.H_START_DT, self.H_END_DT, self.prefix), None)

    def test_valid_data(self):
        with requests_mock.Mocker() as m:
            m.get(self.mock_url, json=self.mock_response)
            self.assertEqual(req_hydrodata(['05463500'], self.H_START_DT, self.H_END_DT, self.prefix),
                             self.valid_return)

    def test_bad_list(self):
        self.assertEqual(req_hydrodata(['x'], self.H_START_DT, self.H_END_DT, self.prefix), None)
        self.assertEqual(req_hydrodata([123456, 100], self.H_START_DT, self.H_END_DT, self.prefix), None)
        self.assertEqual(req_hydrodata([], self.H_START_DT, self.H_END_DT, self.prefix), None)

    def test_bad_url(self):
        self.assertEqual(req_hydrodata(self.sites, self.H_START_DT, self.H_END_DT, 'badurl.noob'), None)
        self.assertEqual(req_hydrodata(self.sites, self.H_START_DT, self.H_END_DT, ''), None)


class TestParseHydroData(unittest.TestCase):
    def setUp(self):
        self.mock_data = [{"sourceInfo": {
            "siteName": "Black Hawk Creek at Hudson, IA",
            "siteCode": [{"value": "05463500", "network": "NWIS", "agencyCode": "USGS"}],
            "timeZoneInfo": {"defaultTimeZone": {"zoneOffset": "-06:00", "zoneAbbreviation": "CST"},
                             "daylightSavingsTimeZone": {
                                 "zoneOffset": "-05:00", "zoneAbbreviation": "CDT"},
                             "siteUsesDaylightSavingsTime": True}, "geoLocation": {
                "geogLocation": {"srs": "EPSG:4326", "latitude": 42.4077639, "longitude": -92.4632451},
                "localSiteXY": []},
            "note": [], "siteType": [], }, "variable": {"variableCode": [], "variableName": "Streamflow, ft&#179;/s",
                                                        "variableDescription": "Discharge, cubic feet per second",
                                                        "valueType": "Derived Value", "unit": {"unitCode": "ft3/s"},
                                                        "note": [], }, "values": [{"value": [{
            "value": "446", "qualifiers": ["A"], "dateTime": "2008-05-20T00:00:00.000-05:00"}, {
            "value": "446", "qualifiers": ["A"], "dateTime": "2008-05-20T00:15:00.000-05:00"}, {
            "value": "446", "qualifiers": ["A"], "dateTime": "2008-05-20T00:30:00.000-05:00"}]}]}]

        self.mock_data_missing_points = self.mock_data = [{"sourceInfo": {
            "siteName": "Black Hawk Creek at Hudson, IA",
            "siteCode": [{"value": "05463500", "network": "NWIS", "agencyCode": "USGS"}],
            "timeZoneInfo": {"defaultTimeZone": {"zoneOffset": "-06:00", "zoneAbbreviation": "CST"},
                             "daylightSavingsTimeZone": {
                                 "zoneOffset": "-05:00", "zoneAbbreviation": "CDT"},
                             "siteUsesDaylightSavingsTime": True}, "geoLocation": {
                "geogLocation": {"srs": "EPSG:4326", "latitude": 42.4077639, "longitude": -92.4632451},
                "localSiteXY": []},
            "note": [], "siteType": [], }, "variable": {"variableCode": [], "variableName": "Streamflow, ft&#179;/s",
                                                        "variableDescription": "Discharge, cubic feet per second",
                                                        "valueType": "Derived Value", "unit": {"unitCode": "ft3/s"},
                                                        "note": [], }, "values": [{"value": [{
            "value": "446", "qualifiers": ["A"], "dateTime": "2008-05-20T00:00:00.000-05:00"}, {
            "value": "446", "qualifiers": ["A"], "dateTime": "2008-05-20T00:15:00.000-05:00"}, {
            "value": "446", "qualifiers": ["A"], "dateTime": "2008-05-20T00:30:00.000-05:00"}, {
            "value": "834", "qualifiers": ["A"], "dateTime": "2008-05-20T01:30:00.000-05:00"}]}]}]

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
                "time": "00:30:00",
                "time_mili": 1211261400000.0,
                "value": "446"
            }]

        #  Contains 3 missing "dummy" points for times between
        #  1211261400000.0 and 1211265000000.0 (incrementing by 900000).
        self.mock_parsed_data_missing = [
            {'key': '05463500', 'name': 'Black Hawk Creek at Hudson, IA', 'date': '2008-05-20', 'time': '00:00:00',
             'timezone': 'CST', 'time_mili': 1211259600000.0, 'value': '446'},
            {'key': '05463500', 'name': 'Black Hawk Creek at Hudson, IA', 'date': '2008-05-20', 'time': '00:15:00',
             'timezone': 'CST', 'time_mili': 1211260500000.0, 'value': '446'},
            {'key': '05463500', 'name': 'Black Hawk Creek at Hudson, IA', 'date': '2008-05-20', 'time': '00:30:00',
             'timezone': 'CST', 'time_mili': 1211261400000.0, 'value': '446'},
            {'key': '05463500', 'name': 'Black Hawk Creek at Hudson, IA', 'date': '2008-05-20', 'time': '00:45:00',
             'timezone': 'CST', 'time_mili': 1211262300000.0, 'value': 'NA'},
            {'key': '05463500', 'name': 'Black Hawk Creek at Hudson, IA', 'date': '2008-05-20', 'time': '01:00:00',
             'timezone': 'CST', 'time_mili': 1211263200000.0, 'value': 'NA'},
            {'key': '05463500', 'name': 'Black Hawk Creek at Hudson, IA', 'date': '2008-05-20', 'time': '01:15:00',
             'timezone': 'CST', 'time_mili': 1211264100000.0, 'value': 'NA'},
            {'key': '05463500', 'name': 'Black Hawk Creek at Hudson, IA', 'date': '2008-05-20', 'time': '01:30:00',
             'timezone': 'CST', 'time_mili': 1211265000000.0, 'value': '834'}]

    def test_empty_data(self):
        self.assertEqual(parse_hydrodata([]), [])
        self.assertEqual(parse_hydrodata(None), [])

    def test_data_not_list(self):
        self.assertEqual(parse_hydrodata({}), [])

    def test_valid_data(self):
        ret = parse_hydrodata(self.mock_data)[0]
        self.assertEqual(ret["key"], self.mock_parsed_data[0]["key"])
        self.assertEqual(ret["name"], self.mock_parsed_data[0]["name"])
        self.assertEqual(ret["date"], self.mock_parsed_data[0]["date"])
        self.assertEqual(ret["time"], self.mock_parsed_data[0]["time"])
        self.assertAlmostEqual(ret["time_mili"], self.mock_parsed_data[0]["time_mili"], delta = 100000000)
        self.assertEqual(ret["value"], self.mock_parsed_data[0]["value"])

    def test_valid_data_missing_count(self):
        ret = parse_hydrodata(self.mock_data_missing_points)
        self.assertEqual(len(ret), len(self.mock_parsed_data_missing))

    def test_valid_data_missing_value(self):
        ret = parse_hydrodata(self.mock_data_missing_points)
        self.assertEqual(ret[3]['value'], 'NA')

    def test_valid_missing_timemilli(self):
        start_date = "2008-05-20"
        start_time = "00:00:00"
        dt = datetime.strptime(start_date + ' ' + start_time, '%Y-%m-%d %H:%M:%S')
        dt_ms = time.mktime(dt.timetuple()) * 1000
        ret = parse_hydrodata(self.mock_data_missing_points)
        for dp in ret:
            self.assertAlmostEqual(dt_ms, dp['time_mili'])
            dt_ms += 900000
