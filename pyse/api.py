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
from string import Formatter

from .utils import get_json, add_url_parameter
from .types import base_filters, default_query_args
from .queries import queries

api_base_url = "https://api.stackexchange.com/2.2/"

# FIXME: Needs tests
def query(site, endpoint, **parameters):
    # FIXME: Defaults, Descriptions
    """
    Query the Stack Exchange API.

    :param site: Stack Exchange site to query
    :param endpoint: URL endpoint of query
    :param parameters: keyword arguments for parameters in API request. if any
        keyword arguments match a default defined in
        `stackexchange.types.default_query_args`, it is ignored for the purpose
        of the query.

    Keyword Arguments:
        :keyword page: page of results to return. defaults to 1
        :keyword pagesize: size of each page of results. defaults to 30
        :keyword fromdate: start of time range for results, inclusive. stored as a
            unix timestamp
        :keyword todate: end of time range for results, inclusive. stored
            as a unix timestamp
        :keyword order: order to sort results in. one of `desc`, `asc`
        :keyword sort: criteria with which to sort items.
            one of `activity`, `votes`, `creation`, `hot`, `week`, `month`.
            defaults to `activity`
        :keyword min: minimum value of the field specified by sort.
            defaults to -sys.maxsize - 1
        :keyword max: maximum value of the field specified by sort
            defaults to sys.maxsize
        :keyword tagged: list of tags to constrain questions to. this is an
            AND constraint, so all tags in list must match. thus, passing
            more than 5 flags will always result in zero results

    :raises ValueError: if the passed URL endpoint expects a specific keyword
        argument, but did not get one. e.g. queries.questions.by_id.ALL
        expects an `ids` keyword argument.
    """

    # get format argument of endpoint. e.g. the `{ids}` in questions/`{ids}`
    format_args = [tup[1] for tup in Formatter().parse(endpoint) if tup[1]]
    format_dict = {}

    # if format arguments are missing, throw error
    missing_args = [f for f in format_args if f not in parameters.keys()]
    if len(missing_args) > 0:
        if len(missing_args) > 1:
            quoted_arg_names = ', '.join("'" + a + "'" for a in missing_args)
            raise ValueError(f"API endpoint '{endpoint}' missing required keyword arguments {quoted_arg_names}")
        else:
            raise ValueError(f"API endpoint '{endpoint}' missing required keyword argument '{missing_args[0]}'")

    for f in format_args:
        # join lists with semicolons for API use
        if isinstance(parameters[f], list):
            format_dict[f] = ";".join([str(x) for x in parameters[f]])
        else:
            format_dict[f] = parameters[f]


    # format endpoint
    method = queries.method(endpoint)
    endpoint = endpoint.format(**format_dict)

    # build query URL with no parameters
    url = api_base_url + endpoint + "?site=" + site

    # append non-default parameters
    for arg, value in parameters.items():
        if default_query_args[arg.upper()] != value and arg not in format_args:
            url = add_url_parameter(url, arg, value)

    if method == "GET":
        return get_json(url)

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
        url = add_url_parameter(url, "include", include_string)

    if len(excludes) > 0:
        exclude_string = ";".join(excludes)
        url = add_url_parameter(url, "exclude", exclude_string)


    if base is not base_filters.DEFAULT:
        url = add_url_parameter(url, "base", base)

    filter_json = get_json(url)

    if "error_id" in filter_json:
        raise ValueError(f"{filter_json['error_name']} {filter_json['error_id']}: {filter_json['error_message']}")

    return filter_json["items"][0]["filter"]
