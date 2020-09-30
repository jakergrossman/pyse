import requests
import json
from sys import maxsize

from .utils import get_json, add_url_parameter
from .models import base_filters

base_url = "https://api.stackexchange.com/2.2/"

def query_questions(site, page=1, pagesize=30, fromdate=0, todate=maxsize,
                    order="desc", sort="activity", min=-maxsize - 1,
                    max=maxsize, tagged=[]):
    # FIXME: Defaults, Descriptions
    """
    Query the Stack Exchange API for questions

    Args:
        site (string):  the Stack Exchange site to query
        page (int):     the page of results to return. defaults to 1
        pagesize (int): the size of each page of results. defaults to 30
        fromdate (int): FIXME
        todate (int):   FIXME
        order (string): order to sort results in. one of `desc`, `asc`
        sort (string):  the criteria with which to sort items.
            one of `activity`, `votes`, `creation`, `hot`, `week`, `month`.
            defaults to `activity`
        min (int):      the minimum value of the field specified by sort.
            defaults to -sys.maxsize - 1
        max (int):      the maximum value of the field specified by sort
            defaults to sys.maxsize
        tagged (list):  the list of tags to constrain questions to. this is an
            AND constraint, so all tags in list must match. thus, passing
            more than 5 flags will always result in zero results
    """
    url = base_url + "questions?site=" + site

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

    Args:
        base:     base filter
        includes: list of fields to include, in addition to the base filter
        excludes: list of fields to exclude from the base filter
        unsafe:   whether or not the returned filter
                  string is inline-able in HTML without
                  script-injection concerns
    Returns:
        string: a filter to pass to other API queries

    Raises:
        ValueError: If `base` is not a valid base filter
    """
    unsafe_string  = "true" if unsafe else "false"
    url = base_url + "filters/create?unsafe=" + unsafe_string

    # append applicable paramaters
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
