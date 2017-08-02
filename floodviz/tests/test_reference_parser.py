from floodviz import reference_parser

import json
import unittest
from unittest import mock


class TestReferenceParser(unittest.TestCase):

    def setUp(self):

        self.mock_reference = json.dumps({"target_epsg": "EPSG:2794",
                               "site_ids": ["05463500", "05471050", "05420680", "05479000", "05484000", "05481000", "05486000", "05421000",
                                            "05485500", "05455100", "05470500", "05451500", "05458000", "05471000", "05462000", "05457700", "05458500",
                                            "05470000", "05484500", "05481300", "05464220", "05458900", "05485605", "05463000", "05471200", "05476750",
                                            "05411850", "05454220", "05481950", "05416900", "05464500", "05487470"],
                               "display_sites": ["05471200", "05476750", "05411850", "05462000"],
                               "bbox": [-95.3, 39.8, -91, 43.6],
                               "startDate": "2008-06-05",
                               "endDate": "2008-06-15",
                               "peak": {
                                   "site": "05462000",
                                   "dv_date": "2008-06-09"
                               },
                               "reference": {
                                   "type": "FeatureCollection",
                                   "crs": {
                                       "type": "name",
                                       "properties": {
                                           "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                                       }
                                   },
                                   "features": [
                                       {
                                           "type": "Feature",
                                           "id": 0,
                                           "properties": {
                                               "gnis_id": " ",
                                               "gnis_name": " ",
                                               "reftype": "rivers"
                                           },
                                           "geometry": {
                                               "type": "MultiLineString",
                                               "coordinates": []
                                           }
                                       },
                                       {
                                           "type": "Feature",
                                           "geometry": {
                                               "type": "Point",
                                               "coordinates": [
                                               ]
                                           },
                                           "properties": {
                                               "name": "Cedar Rapids IA",
                                               "country.etc": "IA",
                                               "pop": "123243",
                                               "capital": "0",
                                               "reftype": "city"
                                           }
                                       },
                                       {
                                           "type": "Feature",
                                           "geometry": {
                                               "type": "Polygon",
                                               "coordinates": []
                                           },
                                           "properties": {
                                               "group": "12",
                                               "order": " 2951",
                                               "region": "illinois",
                                               "reftype": "politicalBoundaries"
                                           }
                                       }
                                   ]
                               }
                               })

        self.reference_missing_data = json.dumps({
                               "site_ids": ["05463500", "05471050", "05420680", "05479000", "05484000", "05481000", "05486000", "05421000",
                                            "05485500", "05455100", "05470500", "05451500", "05458000", "05471000", "05462000", "05457700", "05458500",
                                            "05470000", "05484500", "05481300", "05464220", "05458900", "05485605", "05463000", "05471200", "05476750",
                                            "05411850", "05454220", "05481950", "05416900", "05464500", "05487470"],
                               "display_sites": ["05471200", "05476750", "05411850", "05462000"],
                               "bbox": [-95.3, 39.8, -91, 43.6],
                               "startDate": "2008-06-05",
                               "endDate": "2008-06-15",
                               "peak": {
                                   "site": "05462000",
                                   "dv_date": "2008-06-09"
                               },
                               "reference": {
                                   "type": "FeatureCollection",
                                   "crs": {
                                       "type": "name",
                                       "properties": {
                                           "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                                       }
                                   },
                                   "features": [
                                       {
                                           "type": "Feature",
                                           "id": 0,
                                           "properties": {
                                               "gnis_id": " ",
                                               "gnis_name": " ",
                                               "reftype": "rivers"
                                           },
                                           "geometry": {
                                               "type": "MultiLineString",
                                               "coordinates": []
                                           }
                                       },
                                       {
                                           "type": "Feature",
                                           "geometry": {
                                               "type": "Point",
                                               "coordinates": [
                                               ]
                                           },
                                           "properties": {
                                               "name": "Cedar Rapids IA",
                                               "country.etc": "IA",
                                               "pop": "123243",
                                               "capital": "0",
                                               "reftype": "city"
                                           }
                                       },
                                       {
                                           "type": "Feature",
                                           "geometry": {
                                               "type": "Polygon",
                                               "coordinates": []
                                           },
                                           "properties": {
                                               "group": "12",
                                               "order": " 2951",
                                               "region": "illinois",
                                               "reftype": "politicalBoundaries"
                                           }
                                       }
                                   ]
                               }
                               })

        self.bad_json = "x"

        self.mock_response = {'epsg': '2794',
                              'site_ids': ['05463500', '05471050', '05420680', '05479000', '05484000', '05481000',
                                           '05486000', '05421000', '05485500', '05455100', '05470500', '05451500',
                                           '05458000', '05471000', '05462000', '05457700', '05458500', '05470000',
                                           '05484500', '05481300', '05464220', '05458900', '05485605', '05463000',
                                           '05471200', '05476750', '05411850', '05454220', '05481950', '05416900',
                                           '05464500', '05487470'],
                              'display_sites': ['05471200', '05476750', '05411850', '05462000'],
                              'bbox': [-95.3, 39.8, -91, 43.6], 'start_date': '2008-06-05', 'end_date': '2008-06-15',
                              'peak_dv_date': '2008-06-09', 'peak_site': '05462000',
                              'city_geojson_data': {'type': 'FeatureCollection', 'features': [
                                  {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': []},
                                   'properties': {'name': 'Cedar Rapids IA', 'country.etc': 'IA', 'pop': '123243',
                                                  'capital': '0', 'reftype': 'city'}}]},
                              'river_geojson_data': '{"type": "FeatureCollection", "features": [{"type": "Feature", "id": 0, "properties": {"gnis_id": " ", "gnis_name": " ", "reftype": "rivers"}, "geometry": {"type": "MultiLineString", "coordinates": []}}]}',
                              'background_geojson_data': '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": []}, "properties": {"group": "12", "order": " 2951", "region": "illinois", "reftype": "politicalBoundaries"}}]}'}

        self.mock_path = "mock/path.json"


    def test_good_data(self):
        with mock.patch('floodviz.reference_parser.open', mock.mock_open(read_data=self.mock_reference)):
            parsed_data = reference_parser.parse_reference_data(self.mock_path)
            self.assertEqual(parsed_data['epsg'], self.mock_response['epsg'])
            self.assertEqual(parsed_data['display_sites'], self.mock_response['display_sites'])
            self.assertEqual(parsed_data['bbox'], self.mock_response['bbox'])
            self.assertEqual(parsed_data['epsg'], self.mock_response['epsg'])
            self.assertEqual(parsed_data['peak_dv_date'], self.mock_response['peak_dv_date'])

    def test_bad_path(self):
        parsed_data = reference_parser.parse_reference_data(self.mock_path)
        self.assertEqual(parsed_data, None)

    def test_missing_field(self):
        with mock.patch('floodviz.reference_parser.open', mock.mock_open(read_data=self.reference_missing_data)):
            parsed_data = reference_parser.parse_reference_data(self.mock_path)
            self.assertEqual(parsed_data, None)

    def test_bad_json(self):
        with mock.patch('floodviz.reference_parser.open', mock.mock_open(read_data=self.bad_json)):
            parsed_data = reference_parser.parse_reference_data(self.mock_path)
            self.assertEqual(parsed_data, None)

    def test_feature_parsing(self):
        with mock.patch('floodviz.reference_parser.open', mock.mock_open(read_data=self.mock_reference)):
            parsed_data = reference_parser.parse_reference_data(self.mock_path)
            self.assertEqual(parsed_data['city_geojson_data']['features'],
                             self.mock_response['city_geojson_data']['features'])
            self.assertEqual(json.loads(parsed_data['river_geojson_data'])['features'],
                             json.loads(self.mock_response['river_geojson_data'])['features'])
            self.assertEqual(json.loads(parsed_data['background_geojson_data'])['features'],
                             json.loads(self.mock_response['background_geojson_data'])['features'])




