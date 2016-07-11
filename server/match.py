# encoding=utf-8
'''
Stores matches found in an index.html diff.

:copyright: (c) 2016 by Martin Grønholdt.
:license: MIT, see LICENSE for more details.
'''


class Match(object):
    """
    Object to store matches for a pattern.
    """
    def __init__(self, pattern):
        """
        Constructor
        """
        self.matches = list()
        self.pattern = pattern

    def add_match(self, string, score):
        """
        Add a match to the list.
        """
        self.matches.append({'string': string, 'score': score})

    def add_matches(self, matches):
        """
        Add a matches from another object.
        """
        if matches is not None:
            self.matches += matches.matches

    def get_dict(self):
        """
        Get a dictionary representation of this match object.
        """
        ret = dict()
        ret['pattern'] = self.pattern.name
        ret['matches'] = self.matches
        return ret
