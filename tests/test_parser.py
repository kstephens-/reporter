import unittest
import reporter.parser as parser


class ApacheLogParserTest(unittest.TestCase):

    def test_parse(self):

        test_cases = [
            ('183.60.212.148 - - [26/Aug/2014:06:26:39 -0600] '
             '"GET /entry/15205 HTTP/1.1" 200 4865 "-" '
             '"Mozilla/5.0 (compatible; EasouSpider; '
             '+http://www.easou.com/search/spider.html)"'),
            ('183.60.212.148 someuser - [26/Aug/2014:06:26:39 -0600] '
             '"GET /entry/15205 HTTP/1.1" 200 4865 "-" '
             '"Mozilla/5.0 (compatible; EasouSpider; '
             '+http://www.easou.com/search/spider.html)"')
        ]
        expected = [
            {'ip': '183.60.212.148',
             'date': '26/Aug/2014:06:26:39 -0600',
             'request': 'GET /entry/15205 HTTP/1.1',
             'status': '200',
             'size': '4865',
             'user_agent': (
                 'Mozilla/5.0 (compatible; EasouSpider; '
                 '+http://www.easou.com/search/spider.html)'
             )},
            None
        ]
        p = parser.ApacheLogParser()
        result = []
        for case in test_cases:
            result.append(p.parse(case))
        self.assertEqual(expected, result)
