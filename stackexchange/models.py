"""
stackexchange.models
~~~~~~~~~~~~~~~~~~~~

This module contains the primary objects that power the Stack Exchange API

:copyright: (c) 2020 by Jake Grossman
:license: MIT, see LICENSE for more details.
"""

from .structures import LookupDict

_user_classes = [
    "user",
    "shallow_user",
    "network_user"
]

user_classes = LookupDict(name="user_classes")

def _init_user_classes():
    for u in _user_classes:
        setattr(user_classes, u.upper(), u)

_init_user_classes()

class User(object):
    def __init__(user_class, user_info):
        """
        Create a new User

        Args:
            user_type (string): one of user, shallow_user, network_user
            user_info (dict):   a dictionary containing key value pairs about
                the user
        """
        self.user_type = user_class

        for key in user_info:
            setattr(self, key, user_info[key])

class Question(object):
    def __init__(question_info):
        """
        Create a new Question

        Args:
            question_info (dict): a dictionary containing key value pairs about
                the question
        """
        for key in question_info:
            setattr(self, key, question_info[key])

class Answer(object):
    def __init__(answer_info):
        """
        Create a new Answer

        Args:
            answer_info (dict): a dictionary containing key value pairs about
                the question
        """
        for key in question_info:
            setattr(self, key, question_info[key])

_base_filters = [
    "default",  # default for each query type
    "withbody", # BaseFilter.DEFAULT + *.body fields
    "none",     # No filters
    "total"    # Only the ".total" filter
]

base_filters = LookupDict(name="base_filters")

def _init_base_filter_types():
    for f in _base_filters:
        setattr(base_filters, f.upper(), f)

_init_base_filter_types()
