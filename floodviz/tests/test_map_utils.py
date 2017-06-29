from floodviz.map_utils import site_dict, get_sites_geojson

import unittest

import requests_mock


class TestSiteDict(unittest.TestCase):

    def setUp(self):
        self.sites = ['05420680', '05463500']
        self.prefix = 'https://waterservices.usgs.gov/nwis/'
        self.url = "https://waterservices.usgs.gov/nwis/site/?format=rdb&sites=05420680,05463500&siteStatus=all"
        self.good_return = [{'agency_cd': 'USGS', 'site_no': '05420680',
                             'station_nm': 'Wapsipinicon River near Tripoli, IA', 'site_tp_cd': 'ST',
                             'dec_lat_va': '42.83609117', 'dec_long_va': '-92.2574003', 'coord_acy_cd': 'F',
                             'dec_coord_datum_cd': 'NAD83', 'alt_va': ' 986.42', 'alt_acy_va': '.01',
                             'alt_datum_cd': 'NGVD29', 'huc_cd': '07080102'},
                            {'agency_cd': 'USGS', 'site_no': '05463500', 'station_nm': 'Black Hawk Creek at Hudson, IA',
                             'site_tp_cd': 'ST', 'dec_lat_va': '42.4077639', 'dec_long_va': '-92.4632451',
                             'coord_acy_cd': 'F', 'dec_coord_datum_cd': 'NAD83', 'alt_va': ' 865.03',
                             'alt_acy_va': '.01', 'alt_datum_cd': 'NGVD29', 'huc_cd': '07080205'}]
        self.mock_missing_huc = ("#\n"
                                 "#\n"
                                 "# US Geological Survey\n"
                                 "# retrieved: 2017-06-28 11:08:49 -04:00	(vaas01)\n"
                                 "#\n"
                                 "# The Site File stores location and general information about groundwater,\n"
                                 "# surface water, and meteorological sites\n"
                                 "# for sites in USA.\n"
                                 "#\n"
                                 "# File-format description:  http://help.waterdata.usgs.gov/faq/about-tab-delimited-"
                                 "output\n"
                                 "# Automated-retrieval info: http://waterservices.usgs.gov/rest/Site-Service.html\n"
                                 "#\n"
                                 "# Contact:   gs-w_support_nwisweb@usgs.gov\n"
                                 "#\n"
                                 "# The following selected fields are included in this output:\n"
                                 "#\n"
                                 "#  agency_cd       -- Agency\n"
                                 "#  site_no         -- Site identification number\n"
                                 "#  station_nm      -- Site name\n"
                                 "#  site_tp_cd      -- Site type\n"
                                 "#  dec_lat_va      -- Decimal latitude\n"
                                 "#  dec_long_va     -- Decimal longitude\n"
                                 "#  coord_acy_cd    -- Latitude-longitude accuracy\n"
                                 "#  dec_coord_datum_cd -- Decimal Latitude-longitude datum\n"
                                 "#  alt_va          -- Altitude of Gage/land surface\n"
                                 "#  alt_acy_va      -- Altitude accuracy\n"
                                 "#  alt_datum_cd    -- Altitude datum\n"
                                 "#  huc_cd          -- Hydrologic unit code\n"
                                 "#\n"
                                 "agency_cd	site_no	station_nm	site_tp_cd	dec_lat_va	dec_long_va	coord_acy_cd	"
                                 "dec_coord_datum_cd	alt_va	alt_acy_va	alt_datum_cd	huc_cd\n"
                                 "5s	15s	50s	7s	16s	16s	1s	10s	8s	3s	10s	16s\n"
                                 "USGS	05420680	Wapsipinicon River near Tripoli, IA	ST	42.83609117	-92.2574003	F"
                                 "	NAD83	 986.42	.01	NGVD29	07080102\n"
                                 "USGS	05463500	Black Hawk Creek at Hudson, IA	ST	42.4077639	-92.4632451	F	"
                                 "NAD83	 865.03	.01	NGVD29")
        self.missing_huc_return = [{'agency_cd': 'USGS', 'site_no': '05420680',
                             'station_nm': 'Wapsipinicon River near Tripoli, IA', 'site_tp_cd': 'ST',
                             'dec_lat_va': '42.83609117', 'dec_long_va': '-92.2574003', 'coord_acy_cd': 'F',
                             'dec_coord_datum_cd': 'NAD83', 'alt_va': ' 986.42', 'alt_acy_va': '.01',
                             'alt_datum_cd': 'NGVD29', 'huc_cd': '07080102'},
                            {'agency_cd': 'USGS', 'site_no': '05463500', 'station_nm': 'Black Hawk Creek at Hudson, IA',
                             'site_tp_cd': 'ST', 'dec_lat_va': '42.4077639', 'dec_long_va': '-92.4632451',
                             'coord_acy_cd': 'F', 'dec_coord_datum_cd': 'NAD83', 'alt_va': ' 865.03',
                             'alt_acy_va': '.01', 'alt_datum_cd': 'NGVD29'}]

    def test_empty_list(self):
        self.assertEqual(site_dict([], self.prefix), [])

    def test_good_data(self):
        self.assertEqual(site_dict(self.sites, self.prefix), self.good_return)

    def test_missing_fields(self):
        with requests_mock.Mocker() as m:
            m.get(self.url, text=self.mock_missing_huc)
            self.assertEqual(site_dict(self.sites, self.prefix), self.missing_huc_return)

    def test_bad_status_code(self):
        with requests_mock.Mocker() as m:
            m.get(self.url, status_code=404)
            self.assertEqual(site_dict(self.sites, self.prefix), None)


class TestWriteGeojson(unittest.TestCase):

    def setUp(self):
        self.good_data = [{'agency_cd': 'USGS', 'site_no': '05420680',
                             'station_nm': 'Wapsipinicon River near Tripoli, IA', 'site_tp_cd': 'ST',
                             'dec_lat_va': '42.83609117', 'dec_long_va': '-92.2574003', 'coord_acy_cd': 'F',
                             'dec_coord_datum_cd': 'NAD83', 'alt_va': ' 986.42', 'alt_acy_va': '.01',
                             'alt_datum_cd': 'NGVD29', 'huc_cd': '07080102'},
                          {'agency_cd': 'USGS', 'site_no': '05463500', 'station_nm': 'Black Hawk Creek at Hudson, IA',
                             'site_tp_cd': 'ST', 'dec_lat_va': '42.4077639', 'dec_long_va': '-92.4632451',
                             'coord_acy_cd': 'F', 'dec_coord_datum_cd': 'NAD83', 'alt_va': ' 865.03',
                             'alt_acy_va': '.01', 'alt_datum_cd': 'NGVD29', 'huc_cd': '07080205'}]
        self.missing_huc_data = [{'agency_cd': 'USGS', 'site_no': '05420680',
                                    'station_nm': 'Wapsipinicon River near Tripoli, IA', 'site_tp_cd': 'ST',
                                    'dec_lat_va': '42.83609117', 'dec_long_va': '-92.2574003', 'coord_acy_cd': 'F',
                                    'dec_coord_datum_cd': 'NAD83', 'alt_va': ' 986.42', 'alt_acy_va': '.01',
                                    'alt_datum_cd': 'NGVD29', 'huc_cd': '07080102'},
                                   {'agency_cd': 'USGS', 'site_no': '05463500',
                                    'station_nm': 'Black Hawk Creek at Hudson, IA',
                                    'site_tp_cd': 'ST', 'dec_lat_va': '42.4077639', 'dec_long_va': '-92.4632451',
                                    'coord_acy_cd': 'F', 'dec_coord_datum_cd': 'NAD83', 'alt_va': ' 865.03',
                                    'alt_acy_va': '.01', 'alt_datum_cd': 'NGVD29'}]
        self.good_return = ("{ \"type\": \"FeatureCollection\", \"features\": [ \n"
                            "{ \"type\": \"Feature\",\n"
                            " \"geometry\": {\n"
                            " \"type\": \"Point\",\n"
                            " \"coordinates\" : [-92.2574003, 42.83609117]\n"
                            " },\n"
                            " \"properties\": {\n"
                            " \"name\": \"Wapsipinicon River near Tripoli, IA\",\n"
                            " \"id\": \"05420680\",\n"
                            " \"huc\": \"07080102\" \n"
                            " } \n"
                            " },\n"
                            "{ \"type\": \"Feature\",\n"
                            " \"geometry\": {\n"
                            " \"type\": \"Point\",\n"
                            " \"coordinates\" : [-92.4632451, 42.4077639]\n"
                            " },\n"
                            " \"properties\": {\n"
                            " \"name\": \"Black Hawk Creek at Hudson, IA\",\n"
                            " \"id\": \"05463500\",\n"
                            " \"huc\": \"07080205\" \n"
                            " } \n"
                            " }\n"
                            " ] }")
        self.missing_huc_return = ("{ \"type\": \"FeatureCollection\", \"features\": [ \n"
                                   "{ \"type\": \"Feature\",\n"
                                   " \"geometry\": {\n"
                                   " \"type\": \"Point\",\n"
                                   " \"coordinates\" : [-92.2574003, 42.83609117]\n"
                                   " },\n"
                                   " \"properties\": {\n"
                                   " \"name\": \"Wapsipinicon River near Tripoli, IA\",\n"
                                   " \"id\": \"05420680\",\n"
                                   " \"huc\": \"07080102\" \n"
                                   " } \n"
                                   " },\n"
                                   "{ \"type\": \"Feature\",\n"
                                   " \"geometry\": {\n"
                                   " \"type\": \"Point\",\n"
                                   " \"coordinates\" : [-92.4632451, 42.4077639]\n"
                                   " },\n"
                                   " \"properties\": {\n"
                                   " \"name\": \"Black Hawk Creek at Hudson, IA\",\n"
                                   " \"id\": \"05463500\",\n"
                                   " \"huc\": \"n/a\" \n"
                                   " } \n"
                                   " }\n"
                                   " ] }")

    def test_good_data(self):
        self.assertEqual(get_sites_geojson(self.good_data), self.good_return)

    def test_missing_huc(self):
        self.assertEqual(get_sites_geojson(self.missing_huc_data), self.missing_huc_return)


