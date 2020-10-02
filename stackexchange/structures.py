"""
stackexchange.structures
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
        :param capitalize_leaves: whether or not to capitalize leaves.
        """
        # internal variable used for __repr__
        self._name = name
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
    """
    def __init__(self, dictionary=None, name=None, method=None):
        """
        Create a new URL Tree

        :param dictionary: a dictionary of URLs to use to generate the tree. can
            be nested. URLs can have format parameters in them. Each leaf node
            of the dictionary is uppercased in the URLTree to indicate that it
            is a string value:

                # url dictionary
                urls = {
                    "shop": "site.com/shop",
                    "cart": {
                        "page": "site.com/cart",
                        "checkout": "site.com/cart/checkout"
                    },
                    "user": "site.com/user/{id}"
                }

                # URLTree
                urls = {
                    "SHOP": "site.com/shop",
                    "cart": {
                        "PAGE": "site.com/cart",
                        "CHECKOUT": "site.com/cart/checkout"
                    },
                    "USER": "site.com/user/{id}"
                }

            each node of the tree can be accessed as a property or by subscript:

                key                 value
                -----------------------------------
                urls.SHOP           "site.com/shop"
                urls['SHOP']        "site.com/shop"
                urls.cart.CHECKOUT  "site.com/cart/checkout"
        :param name: name of the URLTree
        :param method: generate a method dictionary instead for the specified
            URL tree. Can be used to create a URLDict with a 'method_lookup'
            field:

                FIXME: MWE from types
        """

        # internal method dictionary, used for self.method()
        self._method = LookupDict()

        # internal variable used for __repr__
        if dictionary is not None:
            for key, value in {k: v for k, v in dictionary.items() if k is not None}.items():
                if isinstance(value, dict):
                    # recursively initialize internal dict
                    setattr(self, key, URLTree(dictionary=value, name=name + '/' + key if name else None, method=method))
                else:
                    # this is a leaf node of the dictionary,
                    if method is not None:
                        # add to internal method dictionary
                        setattr(self._method, value, method)
                    else:
                        setattr(self, key.upper(), value)
        super(URLTree, self).__init__(name=name)

    def __repr__(self):
        return f"<url_tree {self.name}>"

    def method(self, target):
        """
        Get HTTP method of target

        :param target: target URL

        :returns : HTTP method of target URL
        """

        return self._method[target]
