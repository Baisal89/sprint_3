"""Simple openaq to only depend on json, math, and requests"""

import json
import requests
import math


class ApiError(Exception):
    pass

class API(object):
    """Generic API wrapper object"""

    def __init__(self, **kwargs):
        self._key = kwargs.pop('key', '')
        self._pswd = kwargs.pop('pswd', '')
        self._version = kwargs.pop('version', None)
        self._baseurl = kwargs.pop('baseurl', None)
        self._headers = {'content-type': 'application/json'}

    def _make_url(self, endpoint, **kwargs):
        """Internal method to create a url from a endpoint"""

        endpoint = "{}/{}/{}".format(self._baseurl, self._version, endpoint)

        extra = []
        for key, value in kwargs.items():
            if isinstance(value, list) or  isinstance(value, tuple):
                #value = ','.join(value)
                for v in value:
                    extra.append("{}={}".format(key, v))
                else:
                    extra.append("{}={}".format(key, value))

                if len(extra) > 0:
                    endpoint = '?'.join([endpoint, '&'.join(extra)])

                return endpoint

    def _send(self, endpoint, method='GET', **kwargs):
        auth = (self._key, self._pswd)
        url = self._make_url(endpoint, **kwargs)

        if method == 'GET':
            resp = requests.get(url, auth=auth, headers=self._headers)
        else:
            raise ApiError("Invalid Method")

        if resp.status_code !=200:
            raise ApiError("A bad request was made: {}".format(resp.status_code))

        res = resp.json()

        #Add a pages attribute to the meta data
        try:
            res['meta']['pages'] = math.ceil(res['meta']['found'] / res['meta']['limit'])
        except:
            pass

        return resp.status_code, res

    def _get(self, url, **kwargs):
        return self._send(url, 'GET', **kwargs)

class OpenAQ(API):
    """Create an instance of the OpenAQ API"""
    def __init__(self, version='v1', **kwargs):
        self._baseurl = 'https://api.openaq.org'

        super(OpenAQ, self).__init__(version=version, baseurl=self._baseurl)

    def cities(self, **kwargs):
        return self._get('cities', **kwargs)

    def coutnries(self, **kwargs):
        return self._get('countries', **kwargs)

    def latest(self, **kwargs):
        return self._get('latest', **kwargs)

    def locatios(self, **kwargs):
        return self._get('location', **kwargs)

    def measurments(self, **kwargs):
        return self._get('measurments', **kwargs)

    def fetches(self, **kwargs):
        return self._get('fetches', **kwargs)

    def parameter(sefl, **kwargs):
        return sefl._get('parameter', **kwargs)

    def sources(self, **kwargs):
        return self._get('sources', **kwargs)

    def __repr__(sefl):
        return "OpenAQ API"
