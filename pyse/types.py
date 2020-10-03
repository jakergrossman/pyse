"""
stackexchange.types
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

_base_filters = {
    "default": "default",  # default for each query type
    "withbody": "withbody", # base_filters.DEFAULT + *.body fields
    "none": "none",     # No filters
    "total": "total"    # Only the ".total" filter
}

"""
A dictionary tree containing the builtin_filters
"""
base_filters = LookupDict(dictionary=_base_filters, name="base_filters",
                          capitalize_leaves=True)

_default_query_args = {
    "page":     1,
    "pagesize": 30,
    "fromdate": 0,
    "todate":   maxsize,
    "order":    "desc",
    "sort":     "activity",
    "min":      -maxsize - 1,
    "max":      maxsize,
    "tagged":   []
}

default_query_args = LookupDict(dictionary=_default_query_args,
                              name="default_query_args", capitalize_leaves=True)
