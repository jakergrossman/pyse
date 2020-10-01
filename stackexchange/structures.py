"""
stackexchange.structures
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
        return f"<dict_tree '{self._name}'>"

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
        return self.__dict__.update(kwargs)

    def update(self, other):
        for key in other.__dict__:
            if key in self.__dict__:
                # recursively update dictionaries
                if isinstance(self[key], DictTree) and isinstance(other[key], DictTree):
                    self[key].update(other[key])
                elif self[key] != other[key]:
                    # clobber old key
                    setattr(self, key, other[key])
            else:
                setattr(self, key, other[key])

        return self

    def path(self, target):
        for k,v in self.__dict__.items():
            if isinstance(v, dict):
                p = v.path(target)
                if p:
                    return [k] + p
            elif v == target:
                return [k]

# FIXME: Needs tests
class URLTree(DictTree):
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
        # internal variable used for __repr__
        if dictionary is not None:
            for key, value in {k: v for k, v in dictionary.items() if k is not None}.items():
                if isinstance(value, dict):
                    # recursively initialize internal dict
                    setattr(self, key, URLTree(dictionary=value, name=name + '/' + key if name else None, method=method))
                else:
                    # this is a leaf node of the dictionary,
                    if method is not None:
                        setattr(self, key.upper(), method)
                    else:
                        setattr(self, key.upper(), value)
        super(URLTree, self).__init__(name=name)

    def method(self, target):
        target_path = self.path(target)
        temp = self.__dict__['_method']
        for component in target_path:
            temp = temp[component]

        return temp
