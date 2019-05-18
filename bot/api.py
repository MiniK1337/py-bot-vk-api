import urllib.request as urlreq
import urllib.parse as urlparse
import json

from .config import config

def api(method, **kwargs):
    api_url = "https://api.vk.com/method/{{}}?access_token={}&v={}".format(config['access_token'], config['api_version'])

    method_url = api_url.format(method)
    data = {}
    for k, v in kwargs.items():
        if v is not None:
            data[k] = v
    try:
        with urlreq.urlopen(
            url = method_url, 
            data = urlparse.urlencode(data).encode('utf-8')
        ) as r:
            res = json.loads(r.read().decode('utf-8'))
    except Exception as er:
        raise RuntimeError(er)

    if 'error' in res:
        return res['error']

    return res['response']
