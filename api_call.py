import urllib2
from urllib2 import URLError
from simplejson import loads as json_load


def get_data_from_api(url):
    try:
        response = urllib2.urlopen(url)
        response_data = response.read()
    except URLError as e:
        print e.message
        return None
    return json_load(response_data)
