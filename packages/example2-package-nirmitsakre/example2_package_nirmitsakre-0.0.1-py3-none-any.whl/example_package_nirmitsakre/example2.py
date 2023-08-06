import urllib.request
import urllib.parse

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get(self, path, params=None, headers=None):
        url = self.base_url + path
        if params:
            url += '?' + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        return response.read().decode('utf-8')
    
    def post(self, path, data=None, headers=None):
        url = self.base_url + path
        if data:
            data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers)
        response = urllib.request.urlopen(req)
        return response.read().decode('utf-8')
    
    def download(self, path, filename, headers=None):
        url = self.base_url + path
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        with open(filename, 'wb') as f:
            f.write(response.read())

