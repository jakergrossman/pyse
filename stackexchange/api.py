"""
stackexchange.api
~~~~~~~~~~~~~~~~~

This module implements the Stack Exchange API wrapper.

:copyright: (c) 2020 by Jake Grossman
:license: MIT, see LICENSE for more details.
"""
import requests
import json
from sys import maxsize

from .utils import get_json, add_url_parameter
from .types import base_filters
from .types import queries, base_filters

api_base_url = "https://api.stackexchange.com/2.2/"

def query_questions(site, page=1, pagesize=30, fromdate=0, todate=maxsize,
                    order="desc", sort="activity", min=-maxsize - 1,
                    max=maxsize, tagged=[]):
    # FIXME: Defaults, Descriptions
    """
    Query the Stack Exchange API for questions

    :param site: Stack Exchange site to query
    :param page: (optional) page of results to return. defaults to 1
    :param pagesize: (optional) size of each page of results. defaults to 30
    :param fromdate: (optional) start of time range for results, inclusive. stored as a
        unix timestamp
    :param todate: (optional) end of time range for results, inclusive. stored
        as a unix timestamp
    :param order: (optional) order to sort results in. one of `desc`, `asc`
    :param sort: (optional) criteria with which to sort items.
        one of `activity`, `votes`, `creation`, `hot`, `week`, `month`.
        defaults to `activity`
    :param min: (optional) minimum value of the field specified by sort.
        defaults to -sys.maxsize - 1
    :param max: (optional) maximum value of the field specified by sort
        defaults to sys.maxsize
    :param tagged: (optional) list of tags to constrain questions to. this is an
        AND constraint, so all tags in list must match. thus, passing
        more than 5 flags will always result in zero results
    """
    url = api_base_url + "questions?site=" + site

    if page != 1:
        url = add_url_parameter(url, "page", page)

    if pagesize != 30:
        url = add_url_parameter(url, "pagesize", pagesize)

    if fromdate != 0:
        url = add_url_parameter(url, "fromdate", fromdate)

    if todate != maxsize:
        url = add_url_parameter(url, "todate", todate)

    if order != "desc":
        url = add_url_parameter(url, "order", order)

    if sort != "activity":
        url = add_url_parameter(url, "activity", activity)

    if min != -maxsize - 1:
        url = add_url_parameter(url, "min", min)

    if max != maxsize:
        url = add_url_parameter(url, "max", max)

    if tagged != []:
        url = add_url_parameter(url, "tagged", ";".join(tagged))

    return url

def create_filter(base=base_filters.DEFAULT, includes=[], excludes=[], unsafe=False):
    """
    Creates a filter string

    :param base:     base filter
    :param includes: list of fields to include, in addition to the base filter
    :param excludes: list of fields to exclude from the base filter
    :param unsafe:   whether or not the returned filter
              string is inline-able in HTML without
              script-injection concerns
    :returns string: a filter to pass to other API queries

    :raises ValueError: If `base` is not a valid base filter
    """
    unsafe_string  = "true" if unsafe else "false"
    url = api_base_url + "filters/create?unsafe=" + unsafe_string
    # append applicable parameters
    if len(includes) > 0:
        include_string = ";".join(includes)
        url += "include=" + include_string

    if len(excludes) > 0:
        exclude_string = ";".join(excludes)
        url += "&exclude=" + exclude_string

    if base is not base_filters.DEFAULT:
        url += "&base=" + base

    filter_json = get_json(url)

    if "error_id" in filter_json:
        raise ValueError(f"{filter_json['error_name']} {filter_json['error_id']}: {filter_json['error_message']}")

    return filter_json["items"][0]["filter"]
