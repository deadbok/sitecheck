# encoding=utf-8
'''
Pattern container.

:copyright: (c) 2016 by Martin Grønholdt.
:license: MIT, see LICENSE for more details.
'''
import json
from server.pattern import Pattern


class Patterns(object):
    """
    Pattern used for searching an index.html for matches.
    """
    def __init__(self, patterns=None):
        """
        Constructor.
        """
        self.onadd = None
        self.patterns = {}
        if patterns is not None:
            for pattern in patterns:
                self.add(pattern=pattern)

    def register_add_listener(self, listener):
        """
        Register a listener that gets called when a pattern is added.
        """
        self.onadd = listener

    def add(self, pattern=None):
        """
        Add pattern.
        """
        self.patterns[pattern['name']] = Pattern(pattern=pattern)
        if self.onadd is not None:
            self.onadd(self.patterns[pattern['name']])

    def add_by_names(self, names):
        """
        Add a list of pattern objects.
        """
        for name in names:
            self.add(name=name)

    def remove(self, name='', pattern=None):
        """
        Remove pattern.
        """
        if (name != '') and (pattern is None):
            del self.patterns[name]
        elif (name == '') and (pattern is not None):
            del self.patterns[pattern.name]

    def remove_by_names(self, names):
        """
        Remove a list of pattern objects.
        """
        for name in names:
            self.remove(name=name)

    def get_dict_list(self):
        """
        Get a list of all pattern data.
        """
        patterns = list()
        for pattern in self.patterns.values():
            patterns.append(pattern.get_dict())

        return patterns

    def send(self, pattern, state, protocol):
        """
        Send a named pattern.
        """
        if pattern in self.patterns.keys():
            self.patterns[pattern].send(state, protocol)

    def send_removed(self, pattern, state, protocol):
        """
        Send removed message for a pattern.
        """
        response = dict()
        response['version'] = state.server['version']
        response['total'] = len(self.patterns)
        response['type'] = 'pattern'
        response['length'] = -1
        response['data'] = [pattern]
        protocol.sendMessage(json.dumps(response).encode('utf-8'), False)
