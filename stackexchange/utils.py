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
