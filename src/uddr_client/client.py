from .connection import Connection
from .response import Response
from .doh import DOHClient
from .api import APIClient
import json, datetime, os
from typing import Dict, List, Optional
from decouple import config

class Client:
    def __init__(self, **kwargs):
        """Initialize the client.
        
        :param api_key: (Optional) UDDR user's API key if not set in the .env file
        :param client_id: (Optional) UDDR client ID if not set in the .env file
        """
        config_settings = config._load('.env') or {}
        
        api_key = kwargs.get('api_key') or config_settings.get('UDDR_API_KEY')
        client_id = kwargs.get('client_id') or config_settings.get('UDDR_CLIENT_ID')
        
        self.connection = Connection(api_key, client_id)
        
    @staticmethod
    def setup(**kwargs):
        """
        This method stores the user's API key and client ID in their .env file for later use.

        :param api_key: (Optional) The user's UDDR API key.
        :param client_id: (Optional) The user's UDDR client ID.
        """
        env_vars = {
            'UDDR_API_KEY': kwargs.get('api_key'),
            'UDDR_CLIENT_ID': kwargs.get('client_id')
        }

        config_settings = {}

        for key, value in env_vars.items():
            try:
                config(key)
                env_var_exists = True
            except:
                env_var_exists = False

            if value is None:
                if env_var_exists:
                    overwrite = input(f'{key} is already set in .env file. Do you want to overwrite it? (y/n): ')
                    if overwrite.lower() != 'y':
                        value = config_settings[key] = config(key)
                        print('Skipping...')
                    else:
                        value = input(f'Enter a new value for {key}: ')
                else:
                    value = input(f'Enter a value for {key}: ')

            # Set the new key-value pair in-memory
            config_settings[key] = value

            print(f'Successfully set {key}.')

        # Write back the updated key-value pairs to the .env file
        with open('.env', 'w') as f:
            for key, value in config_settings.items():
                f.write(f'{key}={value}\n')

    def doh(self, ioc: str) -> Response:
        return DOHClient(self.connection, ioc)
        
    def api(self) -> Response:
        return APIClient(self.connection)