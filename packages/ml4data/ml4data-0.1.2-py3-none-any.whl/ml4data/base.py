from pathlib import Path
from typing import Any, BinaryIO, Dict, List, Optional, Union

import requests

class APIException(Exception):
    def __init__(self, msg: str, status_code: int):
        self.msg = msg
        self.status_code = status_code

    def __str__(self):
        return "[{status_code}] Error: {msg}".format(status_code=self.status_code,
                                                     msg=self.msg)

class AuthenticationError(APIException):
    def __init__(self, msg: str):
        super(AuthenticationError, self).__init__(msg, 401)


FileType = Union[str, Path, BinaryIO]


class ML4DataClient(object):
    """ Base class for all ML4Data clients
    """
    base_url = 'https://api.ml4data.com/api'
    def __init__(self, token: str):
        self.token = token
        self.session = requests.Session()
        self.session.headers = {"API-Key": self.token,
                                "User-Agent": 'ml4data-client'}

    def _make_request(self,
                      method: str,
                      endpoint: str,
                      params: Optional[Dict[str, str]] = None,
                      data: Optional[Dict[str, Any]] = None,
                      files: Optional[Dict[str, BinaryIO]] = None) -> Any:
        url = self.base_url + endpoint
        resp = self.session.request(url=url,
                                    method=method,
                                    params=params,
                                    data=data,
                                    files=files)
        if resp.status_code != 200:
            if resp.status_code == 401:
                raise AuthenticationError(resp.json()['error']['message'])
            else:
                raise APIException(resp.json()['error']['message'], status_code=resp.status_code)
        res_type = resp.headers['Content-Type']
        if res_type == 'application/json':
            return resp.json()['result']
        else: #if res_type in ['application/pdf', 'image/png', 'image/jpeg']:
            return resp.content

    def _get(self,
             endpoint: str,
             params: Optional[Dict[str, str]] = None) -> Any:
        return self._make_request(method='GET',
                                  endpoint=endpoint,
                                  params=params)

    def _post(self,
              endpoint: str,
              params: Optional[Dict[str, str]] = None,
              data: Optional[Dict[str, Any]] = None,
              files: Optional[Dict[str, BinaryIO]] = None) -> Any:
        return self._make_request(method='POST',
                                  endpoint=endpoint,
                                  params=params,
                                  data=data,
                                  files=files)

    def _send_file(self,
                   endpoint: str,
                   file: FileType,
                   params: Optional[Dict[str, str]] = None) -> Any:
        if isinstance(file, (str, Path)):
            with open(file, 'rb') as fp:
                r = self._post(endpoint=endpoint,
                               params=params,
                               files={'file': fp})
        else: # file-like
            r = self._post(endpoint=endpoint,
                           files={'file': file})
        return r

    def __del__(self):
        self.session.close()
