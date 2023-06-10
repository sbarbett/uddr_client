import requests, json
from typing import Dict, Union, Optional

class AuthError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class Connection:
    def __init__(self, api_key: str):
        self.endpoint = 'https://ddr.ultradns.com/api/protect/ext'
        self.api_key = api_key

    def is_json(self, rstring: str) -> bool:
        try:
            json.loads(rstring)
        except ValueError as e:
            return False
        return True

    def build_headers(self, content_type: str) -> Dict[str, str]:
        result = {'Accept': 'application/json', 'X-API-Key': self.api_key}
        if content_type:
            result['Content-Type'] = content_type
        return result

    def post(self, uri: str, json_data: Optional[str] = None) -> Union[Dict, str]:
        if json_data is not None:
            return self._do_call(uri, 'POST', body=json_data)
        else:
            return self._do_call(uri, 'POST')

    def _do_call(self, uri: str, method: str, params: Optional[Dict] = None, body: Optional[str] = None,
                 files: Optional[str] = None, content_type: str = 'application/json') -> Union[Dict, str]:
        r1 = requests.request(method, self.endpoint+uri, params=params, data=body,
                              headers=self.build_headers(content_type), files=files)
        if r1.status_code == requests.codes.no_content:
            return {}
        elif r1.status_code != requests.codes.ok:
            # or raise an exception
            return {"error": "Server returned status code: {}".format(r1.status_code)}
        elif self.is_json(r1.text):
            return r1.json()
        else:
            return r1.text