# encoding=utf-8
'''
Patterns for searching index.html diff's

:copyright: (c) 2016 by Martin Grønholdt.
:license: MIT, see LICENSE for more details.
'''
import json
from server.match import Match


class Pattern(object):
    """
    Pattern used for searching an index.html for matches.
    """
    def __init__(self, name='', ppattern='', ptype='simple', pattern=None):
        if pattern is None:
            self.name = name
            self.type = ptype
            self.pattern = ppattern
        else:
            self.__dict__ = pattern

    def get_dict(self):
        """
        Create a dictionary.
        """
        return self.__dict__

    def from_dict(self, pattern):
        """
        Set values from a dictionary.
        """
        self.__dict__ = pattern

    def match(self, line, add_all=False):
        """
        Match a line.
        """
        matches = Match(self)
        if self.type == 'simple':
            pos = str.lower(line).find(self.pattern)
            if pos != -1:
                matches.add_match(line[:pos], 'neutral')
                matches.add_match(line[pos:pos + len(self.pattern)], 'good')
                # Process the rest.
                matches.add_matches(self.match(line[pos + len(self.pattern):],
                                               add_all=True))
            elif add_all:
                matches.add_match(line, 'neutral')

        return matches

    def send(self, state, protocol):
        """
        Send the complete data set for this pattern.
        """
        response = dict()
        response['version'] = state.server['version']
        response['total'] = len(state.patterns.patterns)
        response['type'] = 'pattern'
        response['length'] = 1
        response['data'] = [self.get_dict()]
        protocol.sendMessage(json.dumps(response).encode('utf-8'), False)
