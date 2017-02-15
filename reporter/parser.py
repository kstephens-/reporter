import re


class LineParser(object):

    def parse(self, line):
        # package this in some kind of structure
        m = self._fields_re.match(line)
        if m:
            return dict(zip(self._fields, m.groups()))


class ApacheLogParser(LineParser):

    _fields_re = re.compile(
        r'^([\d.]+) - [\w-]+ \[(.*?)\] "(.*?)" (\d+) ([\d-]+) "-" "(.*?)"'
    )
    _fields = ('ip', 'date', 'request', 'status', 'size', 'user_agent')
