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
                 db_file='reporter/data/GeoLite2-City.mmdb',
                 state_country=None):

        self.parser = parser()
        self.geo_reader = db.Reader(db_file)
        self.state_country = state_country

        self.country_count = {}
        self.country_page = {}
        self.state_count = {}
        self.state_page = {}

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
        self._report(self.country_count, self.country_page)

    def state_report(self):
        """ format data for report by state (US) """

        print('{:25s}{:15s}{}'.format(
            'State', 'Count', 'Most visited page'))
        self._report(self.state_count, self.state_page)

    def _report(self, counts, pages):
        """ print report items """

        for key, count in sorted(
                counts.items(),
                key=operator.itemgetter(1),
                reverse=True)[:10]:

            page_iter = (
                (k, v) for k, v in pages[key].items()
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
            record = self._associate_ip(log)
            if not record:
                continue

            # count by country
            self.update_country_count(record['country'])
            self.update_country_page(
                record['country'], record['page']
            )

            # count by state
            self.update_state_count(
                record['country'], record['state']
            )
            self.update_state_page(
                record['country'], record['state'], record['page']
            )

    def update_country_count(self, country):
        """ count requests by country """
        try:
            self.country_count[country] += 1
        except KeyError:
            self.country_count[country] = 1

    def update_country_page(self, country, page):
        """ count page views by country """
        if country not in self.country_page:
            self.country_page[country] = {}
        try:
            self.country_page[country][page] += 1
        except KeyError:
            self.country_page[country][page] = 1

    def update_state_count(self, country, state):
        """ count requests by state, optionally limited by country """
        if self.state_country and \
                country != self.state_country:
            pass
        else:
            try:
                self.state_count[state] += 1
            except KeyError:
                self.state_count[state] = 1

    def update_state_page(self, country, state, page):
        """ count page views by state, optionally limited by country """

        if self.state_country and \
                country != self.state_country:
            pass
        else:
            if state not in self.state_page:
                self.state_page[state] = {}
            try:
                self.state_page[state][page] += 1
            except KeyError:
                self.state_page[state][page] = 1

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

    def _associate_ip(self, record):
        """ request geo data for ip """
        try:
            city = self.geo_reader.city(record['ip'])
        except gerr.AddressNotFoundError:
            return
        method, page, http = record['request'].split(' ')
        und = 'unknown'
        return {
            'ip': record['ip'],
            'country': city.country.name or und,
            'state': city.subdivisions.most_specific.name or und,
            'page': page
        }
