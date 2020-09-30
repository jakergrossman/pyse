"""
stackexchange.utils
~~~~~~~~~~~~~~~~~~~

This module contains utility functions for the Stack Exchange wrapper

:copyright: (c) 2020 by Jake Grossman
:license: MIT, see LICENSE for more details.
"""

import requests
import json

# FIXME: Don't expose
def get_json(url):
    r = requests.get(url)

    if r.status_code == requests.codes.ok:
        j = json.loads(r.text)
        return j
    else:
        # raise exception
        r.raise_for_status()

def add_url_parameter(url, parameter, value):
    return url + "&" + parameter + "=" + str(value)
