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
    """
    def __init__(self, dictionaries=None, name=None, method=None):
        """
        Create a new URL Tree

        :param dictionaries: a list of tuples (a, b), where a is an HTTP request
            type, and b is a LookupDict of URLs that use that HTTP method. This
            is used to generate the internal _method LookupDict to use as a
            lookup table. Example:

            _urls = {
                "GET": {
                    "shop": "site.com/shop",
                    "cart": {
                        "view": "site.com/cart"
                    }
                },
                "POST": {
                    "cart": {
                        "checkout": "site.com/checkout"
                    }
                }
            }

            urls = URLTree(
                dictionaries = [
                        (method, url_dict) for method, url_dict in _urls.items()
                    ],
                name = "urls"
            )

            each node of the tree can be accessed as a property or by subscript.
            additionally, both lower- and upper-case names are allowed.

                key                 value
                -----------------------------------
                urls.SHOP           "site.com/shop"
                urls.shop           "site.com/shop"
                urls['SHOP']        "site.com/shop"
                urls.cart.CHECKOUT  "site.com/cart/checkout"

            the internal _method lookup dictionary can be accessed by the
            ``method()`` method to lookup the HTTP request method for an
            endpoint.

            Example:

                urls.method(urls.shop) -> 'GET'
                urls.method(urls.cart.checkout) -> 'POST'

        :param name: name of the URLTree
        :param method: generate a method dictionary instead for the specified
            URL tree.

        """
        self._method = LookupDict()
        if dictionaries is not None:
            if len(dictionaries) > 1:
                for d_method, d in dictionaries:
                    self.update(URLTree([d]))
                    self._method.update(URLTree([d], method=d_method)._method)
            elif len(dictionaries) == 1:
                dictionary = dictionaries[0]

                # internal variable used for __repr__
                if dictionary is not None:
                    for key, value in {k: v for k, v in dictionary.items() if k is not None}.items():
                        if isinstance(value, dict):
                            # recursively initialize internal dict
                            internal_node = URLTree(dictionaries=[value],
                                                    name=name + '/' + key if
                                                    name else None,
                                                    method=method)

                            setattr(self, key, internal_node)
                            if method is not None:
                                self._method.update(internal_node._method)
                        else:
                            # this is a leaf node of the dictionary,
                            if method is not None:
                                # add to internal method dictionary
                                setattr(self._method, value, method)
                            else:
                                # set both uppercase and lowercase keys
                                setattr(self, key, value)
                                setattr(self, key.upper(), value)

        super(URLTree, self).__init__(name=name)

    def __repr__(self):
        return f"<url_tree {self._name}>"

    def method(self, target):
        """
        Get HTTP method of target

        :param target: target URL

        :returns : HTTP method of target URL
        """
        return self._method[target]
