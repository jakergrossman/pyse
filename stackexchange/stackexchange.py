import requests
import json

def get_json(url):
    r = requests.get(url)

    if r.status_code == requests.codes.ok:
        j = json.loads(r.text)
        return j
    else:
        # raise exception
        r.raise_for_status()

class BaseFilter:
    DEFAULT  = "default"  # default for each query type
    WITHBODY = "withbody" # BaseFilter.DEFAULT + *.body fields
    NONE     = "none"     # No filters
    TOTAL    = "total"    # Only the ".total" filter

def create_filter(includes=[], excludes=[], base=BaseFilter.DEFAULT, unsafe=False):
    """Creates a filter string

    Args:
        includes: list of fields to include
        excludes: list of fields to exclude
        base:     base filter
    Returns:
        string: a filter to pass to other API queries

    Raises:
        ValueError: If `base` is not a valid base filter
    """
    unsafe_string  = "true" if unsafe else "false"
    url = "https://api.stackexchange.com/2.2/filters/create?unsafe=" + unsafe_string

    if len(includes) > 0:
        include_string = ";".join(includes)
        url += "include=" + include_string

    if len(excludes) > 0:
        exclude_string = ";".join(excludes)
        url += "&exclude=" + exclude_string

    if base is not BaseFilter.DEFAULT:
        url += "&base=" + base

    filter_json = get_json(url)

    if "error_id" in filter_json:
        raise ValueError(f"{filter_json['error_name']} {filter_json['error_id']}: {filter_json['error_message']}")

    return filter_json["items"][0]["filter"]
