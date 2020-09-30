"""
stackexchange.models
~~~~~~~~~~~~~~~~~~~~

This module contains the structures used in the Stack Exchange API wrapper

:copyright: (c) 2020 by Jake Grossman
:license: MIT, see LICENSE for more details.
"""
# FIXME: Needs tests
class DictTree(dict):
    """
    Dictionary tree, where each node is either a direct mapping to a value
    (leaf node), or a dictionary sub-tree (internal node).
    """
    def __init__(self, dictionary=None, name=None):
        # FIXME: Needs docstring
        # internal variable used for __repr__
        self._name = name
        if dictionary is not None:
            for key, value in {k: v for k, v in dictionary.items() if k is not None}.items():
                if isinstance(value, dict):
                    # recursively initialize internal dict
                    setattr(self, key, DictTree(dictionary=value, name=name + '/' + key))
                else:
                    # this is a leaf node of the dictionary,
                    setattr(self, key.upper(), value)
        super(DictTree, self).__init__()


    def __repr__(self):
        return f"<lookup '{self._name}'>"

    def __getitem__(self, key):
        # allow fallthrough, default to None
        return self.__dict__.get(key, None)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def keys(self):
        # FIXME: Needs docstring
        # filter out all keys starting with an underscore, those
        # are not directly exposed to the user
        return {k: v for k,v in self.__dict__.items() if not k.startswith("_")}.keys()
