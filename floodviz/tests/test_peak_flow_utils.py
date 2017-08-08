import unittest
import requests_mock
from floodviz.peak_flow_utils import req_peak_data, req_peak_dv_data, parse_peak_data


class PeakflowBaseTest(unittest.TestCase):
    correct_dv_peak_output = [
        {'datetime': '2008-07-05', 'discharge': '430'}
    ]

    correct_historic_peaks_output = [{'peak_dt': '1960-05-26', 'peak_va': '5480'},
                                     {'peak_dt': '1961-06-08', 'peak_va': '1870'},
                                     {'peak_dt': '1962-05-30', 'peak_va': '3780'},
                                     {'peak_dt': '1963-08-07', 'peak_va': '2540'},
                                     {'peak_dt': '1964-05-10', 'peak_va': '2010'},
                                     {'peak_dt': '1965-04-02', 'peak_va': '4230'},
                                     {'peak_dt': '1966-06-13', 'peak_va': '5470'},
                                     {'peak_dt': '1967-06-10', 'peak_va': '4000'},
                                     {'peak_dt': '1968-06-28', 'peak_va': '2000'},
                                     {'peak_dt': '1969-03-19', 'peak_va': '4050'},
                                     {'peak_dt': '1970-05-15', 'peak_va': '3810'},
                                     {'peak_dt': '1971-02-20', 'peak_va': '1900'},
                                     {'peak_dt': '1972-08-04', 'peak_va': '1080'},
                                     {'peak_dt': '1973-04-17', 'peak_va': '4130'},
                                     {'peak_dt': '1974-05-19', 'peak_va': '7340'},
                                     {'peak_dt': '1975-03-18', 'peak_va': '2500'},
                                     {'peak_dt': '1976-04-18', 'peak_va': '1960'},
                                     {'peak_dt': '1977-08-28', 'peak_va': '852'},
                                     {'peak_dt': '1978-03-21', 'peak_va': '2980'},
                                     {'peak_dt': '1979-03-20', 'peak_va': '4700'},
                                     {'peak_dt': '1980-06-04', 'peak_va': '1730'},
                                     {'peak_dt': '1981-08-14', 'peak_va': '1140'},
                                     {'peak_dt': '1982-05-28', 'peak_va': '2780'},
                                     {'peak_dt': '1983-06-29', 'peak_va': '3130'},
                                     {'peak_dt': '1984-05-02', 'peak_va': '3220'},
                                     {'peak_dt': '1984-12-28', 'peak_va': '1120'},
                                     {'peak_dt': '1986-06-30', 'peak_va': '7980'},
                                     {'peak_dt': '1987-08-28', 'peak_va': '2610'},
                                     {'peak_dt': '1987-11-30', 'peak_va': '544'},
                                     {'peak_dt': '1989-02-01', 'peak_va': '1540'},
                                     {'peak_dt': '1990-06-19', 'peak_va': '5580'},
                                     {'peak_dt': '1991-06-16', 'peak_va': '3340'},
                                     {'peak_dt': '1992-04-23', 'peak_va': '1790'},
                                     {'peak_dt': '1993-07-10', 'peak_va': '14300'},
                                     {'peak_dt': '1994-03-06', 'peak_va': '1580'},
                                     {'peak_dt': '1995-05-30', 'peak_va': '1960'},
                                     {'peak_dt': '1996-05-10', 'peak_va': '1410'},
                                     {'peak_dt': '1997-07-24', 'peak_va': '1920'},
                                     {'peak_dt': '1998-06-17', 'peak_va': '4280'},
                                     {'peak_dt': '1999-06-12', 'peak_va': '3820'},
                                     {'peak_dt': '2000-07-05', 'peak_va': '533'},
                                     {'peak_dt': '2001-03-17', 'peak_va': '2350'},
                                     {'peak_dt': '2002-05-30', 'peak_va': '912'},
                                     {'peak_dt': '2003-05-06', 'peak_va': '3160'},
                                     {'peak_dt': '2004-05-24', 'peak_va': '7300'},
                                     {'peak_dt': '2005-05-14', 'peak_va': '2530'},
                                     {'peak_dt': '2006-09-14', 'peak_va': '1740'},
                                     {'peak_dt': '2007-02-02', 'peak_va': '850'},
                                     {'peak_dt': '2007-04-27', 'peak_va': '6850'},
                                     {'peak_dt': '2008-06-01', 'peak_va': '7800'}, ]


class TestReqPeakData(PeakflowBaseTest):
    def setUp(self):
        self.nwis_response = '# \n' \
                             '# U.S. Geological Survey\n' \
                             '# National Water Information System\n' \
                             '# Retrieved: 2017-07-03 14:37:04 EDT\n' \
                             '#\n' \
                             '# ---------------------------------- WARNING -----------------------------------\n' \
                             '# Some of the data that you have obtained from this U.S. Geological Survey da...\n' \
                             '# ... LOTS OF COMMENT LINES ...\n' \
                             '#   6 ... Gage datum changed during this year\n' \
                             '#\n' \
                             '#\n' \
                             'agency_cd	site_no	peak_dt	peak_tm	peak_va	peak_cd	gage_ht	gage_ht_cd	\
                             year_last_pk	ag_dt	ag_tm	ag_gage_ht	ag_gage_ht_cd\n' \
                             '5s	15s	10d	6s	8s	27s	8s	13s	4s	10d	6s	8s	11s\n' \
                             'USGS	05481950	1960-05-26		5480		14.05\n' \
                             'USGS	05481950	1961-06-08		1870		11.05\n' \
                             'USGS	05481950	1962-05-30		3780		12.90\n' \
                             'USGS	05481950	1963-08-07		2540		11.80\n' \
                             'USGS	05481950	1964-05-10		2010		11.25	2		1964-06-23		11.70\n' \
                             'USGS	05481950	1965-04-02		4230		13.25\n' \
                             'USGS	05481950	1966-06-13		5470		14.04\n' \
                             'USGS	05481950	1967-06-10		4000		13.11\n' \
                             'USGS	05481950	1968-06-28		2000		11.24\n' \
                             'USGS	05481950	1969-03-19		4050		13.04\n' \
                             'USGS	05481950	1970-05-15		3810		12.97\n' \
                             'USGS	05481950	1971-02-20		1900	2	13.35	1\n' \
                             'USGS	05481950	1972-08-04		1080		8.70\n' \
                             'USGS	05481950	1973-04-17		4130		12.94\n' \
                             'USGS	05481950	1974-05-19		7340		14.69\n' \
                             'USGS	05481950	1975-03-18		2500	2	11.61	1\n' \
                             'USGS	05481950	1976-04-18		1960		9.62\n' \
                             'USGS	05481950	1977-08-28		852		7.81\n' \
                             'USGS	05481950	1978-03-21		2980		11.38\n' \
                             'USGS	05481950	1979-03-20		4700		13.88\n' \
                             'USGS	05481950	1980-06-04		1730		9.02\n' \
                             'USGS	05481950	1981-08-14		1140		7.71\n' \
                             'USGS	05481950	1982-05-28		2780		11.32\n' \
                             'USGS	05481950	1983-06-29		3130		12.41\n' \
                             'USGS	05481950	1984-05-02		3220		11.76\n' \
                             'USGS	05481950	1984-12-28		1120		7.66\n' \
                             'USGS	05481950	1986-06-30		7980		14.73\n' \
                             'USGS	05481950	1987-08-28		2610		11.50\n' \
                             'USGS	05481950	1987-11-30		544		6.34	2		1988-02-01		6.91	1\n' \
                             'USGS	05481950	1989-02-01		1540	2	11.35	1\n' \
                             'USGS	05481950	1990-06-19		5580		14.20\n' \
                             'USGS	05481950	1991-06-16		3340		11.96\n' \
                             'USGS	05481950	1992-04-23		1790		9.76\n' \
                             'USGS	05481950	1993-07-10		14300		16.58\n' \
                             'USGS	05481950	1994-03-06		1580		9.24\n' \
                             'USGS	05481950	1995-05-30		1960		10.12\n' \
                             'USGS	05481950	1996-05-10		1410		8.88\n' \
                             'USGS	05481950	1997-07-24		1920		9.97	2		1997-02-20		10.50	1\n' \
                             'USGS	05481950	1998-06-17		4280		13.20\n' \
                             'USGS	05481950	1999-06-12		3820		12.36\n' \
                             'USGS	05481950	2000-07-05		533		6.36\n' \
                             'USGS	05481950	2001-03-17		2350		10.90\n' \
                             'USGS	05481950	2002-05-30		912		7.55	2		2002-05-13		7.70\n' \
                             'USGS	05481950	2003-05-06		3160		11.99\n' \
                             'USGS	05481950	2004-05-24		7300		14.59\n' \
                             'USGS	05481950	2005-05-14		2530		11.19\n' \
                             'USGS	05481950	2006-09-14	04:30	1740		9.47\n' \
                             'USGS	05481950	2007-02-02		850		13.86\n' \
                             'USGS	05481950	2007-04-27		6850		13.86\n' \
                             'USGS	05481950	2008-06-01		7800		14.51'

        self.correct_outupt = self.correct_historic_peaks_output

        self.prefix = 'http://example.com/'
        self.end_date = '2008-07-05'
        self.site = '05481950'
        self.mock_url = self.prefix + '?site_no=' + self.site + '&agency_cd=USGS&format=rdb&end_date=' + self.end_date

    def test_bad_status_code(self):
        with requests_mock.Mocker() as m:
            m.get(self.mock_url, status_code=404)
            self.assertEqual(req_peak_data(self.site, self.end_date, self.prefix), None)

    def test_valid_data(self):
        with requests_mock.Mocker() as m:
            m.get(self.mock_url, text=self.nwis_response)
            self.assertEqual(req_peak_data(self.site, self.end_date, self.prefix), self.correct_outupt)


class TestReqPeakDVData(PeakflowBaseTest):
    def setUp(self):
        self.nwis_response = '# ---------------------------------- WARNING ----------------------------------------\n' \
                             '# Provisional data are subject to revision. Go to\n' \
                             '# http://help.waterdata.usgs.gov/...provisional-data-statement for more information.\n' \
                             '#\n' \
                             '# File-format des...on: http://help.waterdata.usgs.gov/faq/about-tab-delimited-output\n' \
                             '# Autom...\n' \
                             '#\n' \
                             '# ... LOTS OF COMMENT LINES ...\n' \
                             '#\n' \
                             '# Data-value qualification codes included in this output:\n' \
                             '#     A  Approved for publication -- Processing and review completed.\n' \
                             '#\n' \
                             'agency_cd	site_no	datetime	43051_00060_00003	43051_00060_00003_cd\n' \
                             '5s	15s	20d	14n	10s\n' \
                             'USGS	05481950	2008-07-05	430	A\n'

        self.correct_output = self.correct_dv_peak_output

        self.prefix = 'http://example.com/'
        self.date = '2008-07-05'
        self.site = '05481950'
        # http://example.com/dv/?format=rdb&sites=05481950&startDT=2008-07-05&endDT=2008-07-05&siteStatus=all
        self.mock_url = self.prefix + 'dv/' '?format=rdb&sites=' + self.site + '&startDT=' + self.date + '&endDT=' + self.date + '&siteStatus=all'

    def test_bad_status_code(self):
        with requests_mock.Mocker() as m:
            m.get(self.mock_url, status_code=404)
            self.assertEqual(req_peak_dv_data(self.site, self.date, self.prefix), None)

    def test_valid_data(self):
        with requests_mock.Mocker() as m:
            m.get(self.mock_url, text=self.nwis_response)
            self.assertEqual(req_peak_dv_data(self.site, self.date, self.prefix), self.correct_output)


class TestParsePeakData(PeakflowBaseTest):
    def setUp(self):
        self.mock_peak_in = self.correct_historic_peaks_output
        self.mock_dv_in = self.correct_dv_peak_output

        self.valid_parsed = [{'label': '1960', 'value': 5480},
                             {'label': '1961', 'value': 1870},
                             {'label': '1962', 'value': 3780},
                             {'label': '1963', 'value': 2540},
                             {'label': '1964', 'value': 2010},
                             {'label': '1965', 'value': 4230},
                             {'label': '1966', 'value': 5470},
                             {'label': '1967', 'value': 4000},
                             {'label': '1968', 'value': 2000},
                             {'label': '1969', 'value': 4050},
                             {'label': '1970', 'value': 3810},
                             {'label': '1971', 'value': 1900},
                             {'label': '1972', 'value': 1080},
                             {'label': '1973', 'value': 4130},
                             {'label': '1974', 'value': 7340},
                             {'label': '1975', 'value': 2500},
                             {'label': '1976', 'value': 1960},
                             {'label': '1977', 'value': 852},
                             {'label': '1978', 'value': 2980},
                             {'label': '1979', 'value': 4700},
                             {'label': '1980', 'value': 1730},
                             {'label': '1981', 'value': 1140},
                             {'label': '1982', 'value': 2780},
                             {'label': '1983', 'value': 3130},
                             {'label': '1984', 'value': 3220},
                             {'label': '1986', 'value': 7980},
                             {'label': '1987', 'value': 2610},
                             {'label': '1989', 'value': 1540},
                             {'label': '1990', 'value': 5580},
                             {'label': '1991', 'value': 3340},
                             {'label': '1992', 'value': 1790},
                             {'label': '1993', 'value': 14300},
                             {'label': '1994', 'value': 1580},
                             {'label': '1995', 'value': 1960},
                             {'label': '1996', 'value': 1410},
                             {'label': '1997', 'value': 1920},
                             {'label': '1998', 'value': 4280},
                             {'label': '1999', 'value': 3820},
                             {'label': '2000', 'value': 533},
                             {'label': '2001', 'value': 2350},
                             {'label': '2002', 'value': 912},
                             {'label': '2003', 'value': 3160},
                             {'label': '2004', 'value': 7300},
                             {'label': '2005', 'value': 2530},
                             {'label': '2006', 'value': 1740},
                             {'label': '2007', 'value': 6850},
                             {'label': '2008', 'value': 7800}]

    def test_empty_data(self):
        self.assertEqual(parse_peak_data([], []), [])

    def test_data_not_list(self):
        self.assertEqual(parse_peak_data({}, {}), [])
        self.assertEqual(parse_peak_data(None, None), [])

    def test_valid_data(self):
        self.assertEqual(parse_peak_data(self.mock_peak_in, self.mock_dv_in), self.valid_parsed)
