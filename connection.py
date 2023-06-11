import requests

class AuthError(Exception):
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return repr(self.message)
        
class Connection:
    def __init__(self, api_key):
        self.endpoint = 'https://ddr.ultradns.com/api/protect/ext'
        self.api_key = api_key
        
    def _build_headers(self):
        return {
            'Content-Type': 'application/json',
            'X-API-Key': self.api_key
        }
        
    def post(self, uri, data=None, accept='application/json'):
        return self._do_call(uri, 'POST', data=data, accept=accept)
        
    def _do_call(self, uri, method, data=None, accept='application/json'):
        headers = self._build_headers()
        headers['Accept'] = accept
        response = requests.request(
            method, 
            self.endpoint+uri, 
            data=data, 
            headers=headers
        )

        # Check for No Content
        if response.status_code == requests.codes.no_content:
            return {}

        # If Accept header is application/pdf, return raw response content
        if accept == 'application/pdf':
            return response.content

        # Attempt to return JSON, if not possible return text.
        try:
            return response.json()
        except ValueError:
            return response.text