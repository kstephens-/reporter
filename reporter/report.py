import re
import operator
import reporter.parser as parser

import geoip2.database as db
import geoip2.errors as gerr


FILTER_RE = (
    r'/(?:[\w\d/-]+)?'
    r'(?:images|css|js|static|robots\.txt|favicon\.ico|.*?\.(?:rss|atom))'
)


class AccessReport(object):

    def __init__(self, parser=parser.ApacheLogParser,
                 db_file=None, db_inst=None,
                 state_country=None):

        self.parser = parser()
        self.state_country = state_country

        if db_file:
            self.geo_reader = db.Reader(db_file)
        elif db_inst:
            self.geo_reader = db_inst
        else:
            raise TypeError("'__init__' missing one required "
                            "argument: db_file or db_inst")

        self.country_count = {}
        self.country_page_count = {}
        self.state_count = {}
        self.state_page_count = {}

        self._request_re = re.compile(FILTER_RE)

    def report(self, path):
        """ run apache access log report """
        self.aggregate(path)

        # country report
        print()
        self.country_report()

        print()
        print()
        # state report
        self.state_report()
        print()

    def country_report(self):
        """ format data for report by country """

        print('{:25s}{:15s}{}'.format(
            'Country', 'Count', 'Most visited page'))
        self._report(self.country_count, self.country_page_count)

    def state_report(self):
        """ format data for report by state (US) """

        print('{:25s}{:15s}{}'.format(
            'State', 'Count', 'Most visited page'))
        self._report(self.state_count, self.state_page_count)

    def _report(self, counts, pages):
        """ print report items """

        for key, count in sorted(
                counts.items(),
                key=operator.itemgetter(1),
                reverse=True)[:10]:

            page_iter = (
                (k, v) for k, v in sorted(pages[key].items())
                if k != '/'
            )
            most_visited, _ = max(
                page_iter, key=operator.itemgetter(1)
            )
            print('{:25s}{:<15d}{}'.format(
                key, count, most_visited
            ))

    def aggregate(self, path):
        """ aggregate statistics by country, state """

        print('Aggregating data for', path)
        for log in self._parse_file(path):
            record = self._associate_ip(log['ip'], log['request'])
            if not record:
                continue

            # count by country
            self._update_count(record['country'], 'country')
            self._update_page_count(
                record['country'], record['page'], 'country'
            )

            # count by state
            if self._country_filter(record['country']):
                continue
            self._update_count(record['state'], 'state')
            self._update_page_count(
                record['state'], record['page'], 'state'
            )

    def _update_count(self, key, type_):
        counts = getattr(self, '{}_count'.format(type_))
        try:
            counts[key] += 1
        except KeyError:
            counts[key] = 1

    def _update_page_count(self, key, page, type_):
        counts = getattr(self, '{}_page_count'.format(type_))
        if key not in counts:
            counts[key] = {}
        try:
            counts[key][page] += 1
        except KeyError:
            counts[key][page] = 1

    def _parse_file(self, path):
        print('Parsing file:', path)
        with open(path) as fd:
            for line in fd:
                fields = self.parser.parse(line.strip())
                if fields and not \
                        self._request_filter(fields['request']):
                    yield fields

    def _request_filter(self, request):
        """ filter based on request path """
        return self._request_re.search(request)

    def _country_filter(self, country):
        """ filter state counts based on country """
        return self.state_country and \
            country != self.state_country

    def _get_city_reocrd(self, ip):
        try:
            return self.geo_reader.city(ip)
        except gerr.AddressNotFoundError:
            return

    def _associate_ip(self, ip, request):
        ukn = 'unknown'
        method, page, http = request.split(' ')
        city = self._get_city_reocrd(ip)
        if city:
            return {
                'ip': ip,
                'country': city.country.name or ukn,
                'state': city.subdivisions.most_specific.name or ukn,
                'page': page
            }
