"""
pyse.api
~~~~~~~~

This module implements the Stack Exchange API wrapper.

:copyright: (c) 2020 by Jake Grossman
:license: MIT, see LICENSE for more details.
"""
import requests
import json
from sys import maxsize
from string import Formatter

from .structures import LookupDict
from .types import filters, default_parameters
from .utils import get_json, raise_request_exception
from .queries import queries

api_base_url = "https://api.stackexchange.com/2.2/"

# FIXME: Needs tests
def query(endpoint, **parameters):
    """
    Query the Stack Exchange API.

    :param site: Stack Exchange site to query
    :param endpoint: URL endpoint of query
    :param parameters: keyword arguments for parameters in API request.

    :raises ValueError: if the passed URL endpoint expects a specific keyword
        argument, but did not get one. e.g. queries.questions.by_id.ALL
        expects an `ids` keyword argument.
    """

    # get format arguments of endpoint. e.g. the `{ids}` in questions/`{ids}`
    format_args = [tup[1] for tup in Formatter().parse(endpoint) if tup[1]]
    format_dict = {}

    # if format arguments are missing, raise exception
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
    method = queries.methods[endpoint]
    endpoint = endpoint.format(**format_dict)

    # build query URL with no parameters
    url = api_base_url + endpoint

    # add parameters
    if len(parameters) > 0:
        # key, value tuples of non-default parameters
        param_components = []
        for p,v in {p: v for (p,v) in parameters.items() if
                    v != default_parameters[p]}.items():
            # join lists with semicolons for API use
            if isinstance(v, list):
                param_components.append((p, ";".join(v)))
            else:
                param_components.append((p, v))

        # construct parameter portion of URL.
        param_string = "?" + "&".join(p+"="+v for p,v in param_components)
        url += param_string

    if method == "GET":
        j = get_json(url)
        j_lookup = LookupDict(data=j, name="response_wrapper")
        return j_lookup
    elif method == "POST":
        raise NotImplementedError("POST not implemented")

    if "error_id" in j:
        raise_request_exception(ValueError, j)

    return j

# FIXME: Needs tests
def create_filter(base=filters.DEFAULT, include=[], exclude=[], unsafe=False):
    """
    Creates a filter string

    :param base:     base filter
    :param include: list of fields to include, in addition to the base filter
    :param exclude: list of fields to exclude from the base filter
    :param unsafe:   whether or not the returned filter
              string is inline-able in HTML without
              script-injection concerns
    :returns string: a filter to pass to other API queries

    :raises ValueError: If `base` is not a valid base filter
    """
    unsafe_string  = "true" if unsafe else "false"
    filter_json = query(queries.filters.CREATE, base=base, include=include,
                        exclude=exclude, unsafe=unsafe_string)

    if "error_id" in filter_json:
        raise_request_exception(ValueError, filter_json)

    return filter_json["items"][0]["filter"]
