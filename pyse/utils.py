"""
pyse.utils
~~~~~~~~~~

This module contains utility functions for the Stack Exchange wrapper

:copyright: (c) 2020 by Jake Grossman
:license: MIT, see LICENSE for more details.
"""

import requests
import json

from .structures import LookupDict

# FIXME: Don't expose
def get_json(url):
    r = requests.get(url)

    # will manually handle bad requests (400) when needed
    if r.status_code == requests.codes.ok or r.status_code == requests.codes.bad:
        j = json.loads(r.text)
        return j
    else:
        # raise exception
        r.raise_for_status()

def raise_request_exception(e, resp):
    raise e(f"{resp['error_name']} {resp['error_id']}: {resp['error_message']}")
