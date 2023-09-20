import requests
from typing import Dict, Union, Optional
from decouple import config

class Connection:
    def __init__(self, api_key: Optional[str] = None, client_id: Optional[str] = None):
        self.api_endpoint = 'https://ddr.ultradns.com/api/protect/ext'
        self.pvt_api_endpoint = 'https://api.ddr.ultradns.com'
        self.doh_endpoint = 'https://rcsv.ddr.ultradns.com'

        if api_key is None:
            try:
                self.api_key = config('UDDR_API_KEY')
            except:
                self.api_key = api_key
        else:
            self.api_key = api_key
            
        if client_id is None:
            try:
                self.client_id = config('UDDR_CLIENT_ID')
            except:
                self.client_id = client_id
        else:
            self.client_id = client_id

    def get(self, uri: str, doh: Optional[bool] = False, pvt: Optional[bool] = False,
            params: Optional[Dict] = None) -> Union[Dict, str, bytes]:
        if doh is True:
            if self.client_id is None:
                raise ValueError("No Client ID provided. Please set it via argument or call Client.setup.")
                
            return self._do_call(self.doh_endpoint+uri+self.client_id, 'GET', accept='application/dns+json', c_type='application/x-www-form-urlencoded', params=params)
        elif pvt is True:
            return self._do_call(self.pvt_api_endpoint+uri, 'GET', c_type='application/x-www-form-urlencoded')
        else:
            return self._do_call(self.api_endpoint+uri, 'GET', c_type='application/x-www-form-urlencoded')
        
    def post(self, uri: str, data: Optional[Union[Dict, str]] = None,
             accept: str = 'application/json', pvt: Optional[bool] = False) -> Union[Dict, str, bytes]:
        if pvt is True:
            return self._do_call(self.pvt_api_endpoint+uri, 'POST', data=data, accept=accept)
        else:
            return self._do_call(self.api_endpoint+uri, 'POST', data=data, accept=accept)
        
    def _do_call(self, uri: str, method: str, 
                 data: Optional[Union[Dict, str]] = None, 
                 accept: str = 'application/json',
                 c_type: str = 'application/json',
                 params: Optional[Dict] = None) -> Union[Dict, str, bytes]:
        if params is None:
            if self.api_key is None:
                raise ValueError("No API Key provided. Please set it via argument or call Client.setup.")
                
            headers = {
                'Content-Type': c_type,
                'X-API-Key': self.api_key
            }
        else:
            headers = { 'Content-Type': c_type }
            
        headers['Accept'] = accept
        response = requests.request(
            method, 
            uri, 
            data=data, 
            headers=headers,
            params=params
        )

        # For debugging
        # print(response.url)

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