"""
pyse.structures
~~~~~~~~~~~~~~~~~~~~

This module contains the structures used in the Stack Exchange API wrapper

:copyright: (c) 2020 by Jake Grossman
:license: MIT, see LICENSE for more details.
"""
# FIXME: Needs tests
class LookupDict(dict):
    """
    A dictionary lookup object.
    """
    def __init__(self, dictionary=None, name=None, capitalize_leaves=False):
        """
        Create a new LookupDict

        :param dictionary:      dictionary to initialize LookupDict with
        :param name:            internal name of LookupDict
        :param capitalize_leaves: whether or not to capitalize leaf keys.
        """
        # internal variable used for __repr__
        self._name = name if name else ""
        if dictionary is not None:
            for key, value in {k: v for k, v in dictionary.items() if k is not None}.items():
                if isinstance(value, dict):
                    # recursively initialize internal dict
                    setattr(self, key, LookupDict(dictionary=value, name=name + '/' + key))
                else:
                    # this is a leaf node of the dictionary,
                    setattr(self, key.upper() if capitalize_leaves else key, value)
        super(LookupDict, self).__init__()

    def __repr__(self):
        return f"<lookup '{self._name}'>"

    def __getitem__(self, key):
        # allow fallthrough, default to None
        return self.__dict__.get(key, None)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def keys(self):
        """
        Shadows dict.keys(). Omits keys starting with an underscore, those are
        not directly exposed
        """
        return {k: v for k,v in self.__dict__.items() if not k.startswith("_")}.keys()

    def update(self, other):
        """
        Updates dictionary with the elements from another dictionary.

        :param other: dictionary to update with
        """
        for key in other.__dict__:
            if key in self.__dict__:
                # recursively update dictionaries
                if isinstance(self[key], LookupDict) and isinstance(other[key], LookupDict):
                    self[key].update(other[key])
                elif self[key] != other[key]:
                    # clobber old attribute
                    setattr(self, key, other[key])
            else:
                setattr(self, key, other[key])

        return self

    def path(self, target):
        """
        Get property path given a target.

        :param target: value to look for

        :returns: a list of property names
        """
        for k,v in self.__dict__.items():
            if isinstance(v, dict):
                p = v.path(target)
                if p:
                    return [k] + p
            elif v == target:
                return [k]

# FIXME: Needs tests
class URLTree(LookupDict):
    """
    A tree of URL endpoints.

    Two components:
        A tree of URL endpoints
        A mapping from URL endpoints to HTTP methods
    """
    def __init__(self, data, name=None):
        """
        Create a new URL Tree

        :param data: the input dictionary. each nested dictionary becomes a
            subtree. the leaf nodes of this nested dictionary are tuples (m, u)
            where:

                m is the HTTP method associated with this URL endpoint
                u is the URL endpoint

        :param name: optional name for root URLTree.
        """

        super(URLTree, self).__init__(name=name)
        self.methods = LookupDict(name="methods")
        self.site_required = LookupDict(name="site_required")
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict):
                    sub_tree = URLTree(
                        data[k],
                        name=name + "/" + k if name else None
                    )

                    # set subtree
                    setattr(self, k, sub_tree)

                    # set method lookup
                    self.methods.update(sub_tree.methods)
                    self.site_required.update(sub_tree.site_required)
                else:
                    # upper- and lower-case allowed
                    setattr(self, k.upper(), v[1])
                    setattr(self, k, v[1])


                    setattr(self.methods, v[1], v[0])

    def __repr__(self):
        return f"<url_tree '{self._name}'>"

    def get_method(self, target):
        """
        Get HTTP method of target

        :param target: target URL

        :returns : HTTP method of target URL
        """
        return self.methods[target]
