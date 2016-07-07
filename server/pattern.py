# encoding=utf-8
'''
Patterns for searching index.html diff's

:copyright: (c) 2016 by Martin Grønholdt.
:license: MIT, see LICENSE for more details.
'''
from server.match import Match


class Pattern(object):
    """
    Pattern used for searching an index.html for matches.
    """
    def __init__(self, pattern='', simple=True):
        self.simple = simple
        self.value = pattern

    def match(self, line, add_all=False):
        """
        Match a line.
        """
        matches = Match(self)
        if self.simple:
            pos = str.lower(line).find(self.value)
            if pos != -1:
                matches.add_match(line[:pos], 'neutral')
                matches.add_match(line[pos:pos + len(self.value)], 'good')
                # Process the rest.
                matches.add_matches(self.match(line[pos + len(self.value):],
                                               add_all=True))
            elif add_all:
                matches.add_match(line, 'neutral')

        return matches
