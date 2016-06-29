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
        if self.simple:
            if string.find(self.value) != -1:
                self.msgs.append({'score': 'good', 'msg': string})
