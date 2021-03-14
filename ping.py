

import re

import requests


# Request the data for a given url
# page contents for a regexp pattern that is expected to be found on the page.
def ping(count=1, url='http://localhost:8080'):
    """
    args:
        status_code(int): error code returned
        response_time(int): the HTTP response time,

    returns: json message,key
    """
    print("Sending GET to: {}".format(url))
    response = requests.get(url)
    response_time = response.elapsed.total_seconds()

    body = response.text
    d = re.search('<title.*?>(.+?)</title>', body, re.IGNORECASE)
    try:
        title = d.group(1)
    except AttributeError:
        title = ''

    message = {
        'id': count,
        'status_code': response.status_code,
        'response_time': response_time,
        'page_title': title,
    }
    key = {'website': url}
    return message, key
