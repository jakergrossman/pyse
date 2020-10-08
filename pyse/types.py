"""
pyse.types
~~~~~~~~~~~~~~~~~~~

This module contains lookup dictionaries for types of objects in the Stack Exchange API

:copyright: (c) 2020 by Jake Grossman
:license: MIT, see LICENSE for more details.
"""

from sys import maxsize
from .structures import LookupDict

_user_classes = {
    "user": "user",
    "shallow_user": "shallow_user",
    "network_user": "network_user"
}

"""
A dictionary tree of User types
"""
user_classes = LookupDict(dictionary=_user_classes, name="user_classes",
                          capitalize_leaves=True)

_filters = {
    "default": "default",  # default for each query type
    "withbody": "withbody", # filters.DEFAULT + *.body fields
    "none": "none",     # No filters
    "total": "total"    # Only the ".total" filter
}

"""
A dictionary tree containing the builtin_filters
"""
filters = LookupDict(dictionary=_filters, name="filters",
                          capitalize_leaves=True)

# TODO: fill dict
_default_parameters = {
    "site":     None,
    "page":     1,
    "pagesize": 30,
    "fromdate": 0,
    "todate":   maxsize,
    "order":    "desc",
    "sort":     "activity",
    "min":      -maxsize - 1,
    "max":      maxsize,
    "tagged":   [],
    "include": [],
    "exclude": [],
    "unsafe": False,
    "base":  filters.DEFAULT,
}

default_parameters = LookupDict(dictionary=_default_parameters,
                              name="default_parameters")
