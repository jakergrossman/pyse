"""
stackexchange.models
~~~~~~~~~~~~~~~~~~~~

This module contains the primary objects that power the Stack Exchange API

:copyright: (c) 2020 by Jake Grossman
:license: MIT, see LICENSE for more details.
"""

from .structures import DictTree

class User(object):
    def __init__(user_class, user_info):
        """
        Create a new User

        :param user_type: one of user, shallow_user, network_user
        :param user_info:   a dictionary containing key value pairs about
            the user
        """
        self.user_type = user_class

        for key in user_info:
            setattr(self, key, user_info[key])

class Question(object):
    def __init__(question_info):
        """
        Create a new Question

        :param question_info: a dictionary containing key value pairs about
            the question
        """
        for key in question_info:
            setattr(self, key, question_info[key])

class Answer(object):
    def __init__(answer_info):
        """
        Create a new Answer

        :param answer_info: a dictionary containing key value pairs about
            the question
        """
        for key in question_info:
            setattr(self, key, question_info[key])
