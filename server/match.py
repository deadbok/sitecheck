# encoding=utf-8
'''
Stores matches found in an index.html diff.

:copyright: (c) 2016 by Martin Grønholdt.
:license: MIT, see LICENSE for more details.
'''


class Match(object):
    def __init__(self):
        self.matches = list()

    def addMatch(self, string, score):
        self.matches.append({'msg': string, 'score': score})
