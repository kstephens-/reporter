import unittest
import reporter.report as report


class AccessReportTest(unittest.TestCase):

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

        r = report.AccessReport()
        result = [
            t for t in test_cases if not r._request_filter(t)
        ]
        self.assertEqual(len_result, len(result))

    def test_associate_ip(self):

        test_case = {
            'ip': '183.60.212.148',
            'date': '26/Aug/2014:06:26:39 -600',
            'request': 'GET /entry/15205 HTTP/1.1',
            'status': '200',
            'size': '4865',
            'user_agent': (
                'Mozilla/5.0 (compatible; EasouSpider; '
                '+http://www.easou.com/search/spider.html)'
            )
        }
        expected = {
            'ip': '183.60.212.148',
            'country': 'China',
            'state': 'Guangdong',
            'page': '/entry/15205'
        }

        r = report.AccessReport()
        result = r._associate_ip(test_case)
        self.assertEqual(expected, result)

    def test_update_country_count(self):

        test_case = [
            'United States',
            'China',
            'China',
            'Australia',
            'France',
            'China',
            'United States'
        ]
        expected = {
            'China': 3,
            'United States': 2,
            'Australia': 1,
            'France': 1
        }
        r = report.AccessReport()
        for t in test_case:
            r.update_country_count(t)
        self.assertEqual(expected, r.country_count)

    def test_update_country_page(self):

        test_case = [
            ('United States', '/entry/15201'),
            ('China',  '/entry/15205'),
            ('China', '/entry/15206'),
            ('Australia', '/entry/15201'),
            ('France', '/entry/15205'),
            ('China', '/entry/15205'),
            ('United States', '/entry/15209')
        ]
        expected = {
            'China': {
                '/entry/15205': 2,
                '/entry/15206': 1
            },
            'United States': {
                '/entry/15201': 1,
                '/entry/15209': 1
            },
            'Australia': {
                '/entry/15201': 1
            },
            'France': {
                '/entry/15205': 1
            }
        }

        r = report.AccessReport()
        for country, page in test_case:
            r.update_country_page(country, page)
        self.assertEqual(expected, r.country_page)

    def test_update_state_count(self):

        test_case = [
            ('United States', 'Washington'),
            ('China', 'Guangdong'),
            ('China', 'Hunan'),
            ('Australia', 'New South Whales'),
            ('France', 'Ile-de-France'),
            ('China', 'Guangdong'),
            ('United States', 'California')
        ]
        expected = {
            'Washington': 1,
            'California': 1
        }

        r = report.AccessReport(state_country='United States')
        for country, state in test_case:
            r.update_state_count(country, state)
        self.assertEqual(expected, r.state_count)

    def test_update_state_page(self):

        test_case = [
            ('United States', 'Washington', '/entry/15201'),
            ('China', 'Guangdong', '/entry/15205'),
            ('China', 'Hunan', '/entry/15206'),
            ('Australia', 'New South Whales', '/entry/15201'),
            ('France', 'Ile-de-France', '/entry/15205'),
            ('China', 'Guangdong', '/entry/15205'),
            ('United States', 'California', '/entry/15209')
        ]
        expected = {
            'Washington': {
                '/entry/15201': 1
            },
            'California': {
                '/entry/15209': 1
            }
        }

        r = report.AccessReport(state_country='United States')
        for country, state, page in test_case:
            r.update_state_page(country, state, page)
        self.assertEqual(expected, r.state_page)
