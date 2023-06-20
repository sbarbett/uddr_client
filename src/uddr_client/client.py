from .connection import Connection
from .response import Response
from .doh import DOHClient
from .api import APIClient
import json, datetime, os
from typing import Dict, List, Optional

class Client:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the client.
        
        :param api_key: (Optional) UDDR user's API key if not set in the environment
        """
        self.connection = Connection(api_key)
        
    @staticmethod
    def setup(api_key: str):
        """
        This method stores the user's API key in their environment for later use.

        :param api_key: The user's UDDR API key.
        """
        if 'UDDR_API_KEY' in os.environ:
            overwrite = input('UDDR_API_KEY is already set. Do you want to overwrite it? (y/n): ')
            if overwrite.lower() != 'y':
                print('Aborting...')
                return

        os.environ['UDDR_API_KEY'] = api_key
        print('UDDR_API_KEY is set.')  

    def doh(self, ioc: str) -> Response:
        return DOHClient(self.connection, ioc)
        
    def api(self) -> Response:
        return APIClient(self.connection)