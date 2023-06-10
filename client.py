from .connection import Connection
import json
from typing import Dict

class Client:
    def __init__(self, api_key: str):
        """Initialize the client.
        
        :param api_key: UDDR user's API keys
        """
        self.connection = Connection(api_key)

    def aggregates(self, query_type: str, **kwargs) -> Dict:
        """
        Query the aggregates endpoint.
        
        This method sends a request to the aggregates endpoint. 
        The endpoint provides aggregate data based on the specified query type.
        
        :param query_type: The type of aggregate query. Accepted values are:
            DOMAIN
            FQDN
            COUNTRY
            TLD
            REGISTRAR
        :param kwargs: Additional parameters. Currently supports 'top_count' 
                       which sets how many aggregate values to get. The default is 25.
        :return: The response from the server.
        :raises ValueError: If query_type is not one of the accepted values or if top_count is not an integer.
        """
        uri = "/aggregates"
        applied_filters = {}

        VALID_QUERY_TYPE = {'DOMAIN', 'FQDN', 'COUNTRY', 'TLD', 'REGISTRAR'}
        if query_type.upper() not in VALID_QUERY_TYPE:
            raise ValueError("aggregates: query_type must be one of %r" % VALID_QUERY_TYPE)

        applied_filters.update({'query_type': query_type.lower()})

        if 'top_count' in kwargs:
            try:
                i = int(kwargs['top_count'])
            except ValueError:
                raise ValueError("aggregates: top_count must be an integer")
            applied_filters.update({'top_count': i})

        return self.connection.post(uri, json.dumps({'applied_filters': applied_filters}))
