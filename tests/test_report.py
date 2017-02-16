import unittest
import unittest.mock as mock
import reporter.report as report


class AccessReportTest(unittest.TestCase):

    def setUp(self):

        city_attrs = {
            'country.name': 'China',
            'subdivision.most_specific.name': 'Guangdong'
        }
        city = mock.MagicMock(**city_attrs)

        db_attrs = {
            'city.return_value': city
        }
        geo_db = mock.MagicMock(**db_attrs)

        self.reporter = report.AccessReport(
            db_inst=geo_db,
            state_country='United States'
        )

    def test_request_filter(self):

        test_cases = [
            'GET /region/19.rss HTTP/1.1',
            'GET /7b0744/css/vegguide-combined.css HTTP/1.1',
            'GET /7b0744/images/ratings/green-3-00.png HTTP/1.1',
            'GET /7b0744/js/vegguide-combined.js HTTP/1.1',
            'GET /entry-images/7578/7578-3879-small.jpg HTTP/1.1',
            'GET /images/cok-logo.png HTTP/1.1',
            '/entry/15205',
            'GET /user-images/552-small.jpg HTTP/1.1',
            'GET /static/opensearch_desc.xml HTTP/1.1',
            'GET /robots.txt HTTP/1.1',
            'GET /favicon.ico HTTP/1.1'
        ]
        len_result = 1

        result = [
            t for t in test_cases
            if not self.reporter._request_filter(t)
        ]
        self.assertEqual(len_result, len(result))

    def test_associate_ip(self):

        test_case = {
            'ip': '183.60.212.148',
            'request': 'GET /entry/15205 HTTP/1.1'
        }
        expected = {
            'ip': '183.60.212.148',
            'country': 'China',
            'state': 'Guangdong',
            'page': '/entry/15205'
        }

        result = self.reporter._associate_ip(
            test_case['ip'], test_case['request']
        )
        self.assertEqual(expected, result)

    def test_update_count(self):

        test_cases = [
            ('country', ['United States', 'China', 'China',
             'Australia', 'France', 'China', 'United States']),
            ('state', ['Washington', 'Washington', 'Delaware',
             'California', 'Washington', 'California'])
        ]
        expected = [
            {'China': 3, 'United States': 2, 'Australia': 1,
             'France': 1},
            {'Washington': 3, 'California': 2, 'Delaware': 1}
        ]

        for type_, data in test_cases:
            for t in data:
                self.reporter._update_count(t, type_)
        self.assertEqual(expected[0], self.reporter.country_count)
        self.assertEqual(expected[1], self.reporter.state_count)

    def test_update_page_count(self):

        test_cases = [
            ('country', [('United States', '/entry/15201'),
             ('China',  '/entry/15205'), ('China', '/entry/15206'),
             ('Australia', '/entry/15201'), ('France', '/entry/15205'),
             ('China', '/entry/15205'), ('United States', '/entry/15209')]),
            ('state', [('Washington', '/entry/15201'),
             ('Washington', '/entry/15205'), ('Delaware', '/entry/15206'),
             ('California', '/entry/15201'), ('Washington', '/entry/15205'),
             ('California', '/entry/15205')])
        ]
        expected = [
            {'China': {'/entry/15205': 2, '/entry/15206': 1},
             'United States': {'/entry/15201': 1, '/entry/15209': 1},
             'Australia': {'/entry/15201': 1},
             'France': {'/entry/15205': 1}},
            {'Washington': {'/entry/15201': 1, '/entry/15205': 2},
             'California': {'/entry/15201': 1, '/entry/15205': 1},
             'Delaware': {'/entry/15206': 1}}
        ]

        for type_, data in test_cases:
            for key, page in data:
                self.reporter._update_page_count(key, page, type_)
        self.assertEqual(expected[0], self.reporter.country_page_count)
        self.assertEqual(expected[1], self.reporter.state_page_count)

    def test_country_filter(self):

        test_case = [
            ('United States', 'Washington'),
            ('China', 'Guangdong'),
            ('China', 'Hunan'),
            ('Australia', 'New South Whales'),
            ('France', 'Ile-de-France'),
            ('China', 'Guangdong'),
            ('United States', 'California')
        ]
        expected = [
            'Washington', 'California'
        ]

        result = [
            t[1] for t in test_case
            if not self.reporter._country_filter(t[0])
        ]
        self.assertEqual(expected, result)
