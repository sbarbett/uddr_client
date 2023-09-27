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
        """
        config_settings = config._load('.env') or {}
        api_key = kwargs.get('api_key') or config_settings.get('UDDR_API_KEY')
        self.connection = Connection(api_key)

    @staticmethod
    def setup(**kwargs):
        """
        This method stores the user's API key in their .env file for later use.

        :param api_key: (Optional) The user's UDDR API key.
        """
        env_var_key = 'UDDR_API_KEY'
        api_key = kwargs.get('api_key')

        # If an .env file doesn't exist, create it
        if not os.path.exists('.env'):
            open('.env', 'a').close()

        # Read the existing content of the .env file
        with open('.env', 'r') as f:
            lines = f.readlines()

        # Check if the env_var_key already exists in the file
        env_var_exists = any(line.startswith(env_var_key + '=') for line in lines)

        if api_key is None:
            if env_var_exists:
                existing_value = config(env_var_key)
                overwrite = input(
                    f'{env_var_key} is already set in .env file as {existing_value}. Do you want to overwrite it? (y/n): ')
                if overwrite.lower() != 'y':
                    api_key = existing_value
                    print('Skipping...')
                else:
                    api_key = input(f'Enter a new value for {env_var_key}: ')
                    print(f'Successfully set {env_var_key}.')
            else:
                api_key = input(f'Enter a value for {env_var_key}: ')
                print(f'Successfully set {env_var_key}.')

        # If the variable already exists, update its value. Otherwise, append it.
        if env_var_exists:
            lines = [line if not line.startswith(env_var_key + '=') else f'{env_var_key}={api_key}\n' for line in lines]
        else:
            lines.append(f'{env_var_key}={api_key}\n')

        # Write the modified content back to the .env file
        with open('.env', 'w') as f:
            f.writelines(lines)

    def doh(self, org_name: Optional[str] = None) -> Response:
        return DOHClient(self.connection, self.api(), org_name)
        
    def api(self) -> Response:
        return APIClient(self.connection)