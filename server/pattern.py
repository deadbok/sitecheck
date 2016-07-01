# encoding=utf-8
'''
Patterns for searching index.html diff's

:copyright: (c) 2016 by Martin Grønholdt.
:license: MIT, see LICENSE for more details.
'''
from match import Match


class Pattern(object):
    """
    Pattern used for searching an index.html for matches.
    """
    def __init__(self, pattern='', simple=True):
        self.simple = simple
        self.value = pattern

    def match(self, string):
        """
        Match a string.
        """
        matches = Match(self)
        if self.simple:
            pos = string.find(self.value)
            if pos != -1:
                matches.add_match(string[:pos], 'neutral')
                matches.add_match(self.value, 'good')
                # Process the rest.
                matches.add_matches(self.match(string[pos + len(self.value):]))

        return matches
