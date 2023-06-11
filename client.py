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
        The data shows the frequency of occurrences of different entities 
        (e.g., domains, country codes, registrars, etc.) in the queried dataset.

        :param query_type: The type of aggregate query. Accepted values are:
            DOMAIN
            FQDN
            COUNTRY
            TLD
            REGISTRAR
        :param kwargs: Additional parameters. Currently supports 'top_count' 
                       which sets how many aggregate values to get. The default is 25.
        :return: An aggregate response {
            :param query_type: The query type that the aggregate is for.
            :param top_items: [{
                :param current_doc_count: integer
                    example: 9116
                :param key: string
                    example: debug.opendns.com
                :param previous_doc_count: integer
                    example: 7151
            }]
        }
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

    def bar(self, query_type: str) -> Dict:
        """
        Query the bar chart endpoint.

        This method sends a request to the bar chart endpoint. 
        The endpoint provides bar chart data based on the specified query type. 
        The bar chart shows how the number of queries changes over time for a specific type of queries.

        :param query_type: The type of bar chart query to perform. Accepted values are:
            BLOCK_QUERIES
            NO_ANSWER_QUERIES
            TOR_PROX_VPN_QUERIES
            SUSPICIOUS_NAMESERVER_QUERIES
        :return: A bar chart response object with the following params.
        {
            :param query_type: The query type that the bar chart is for.
            :param top_items: [{
                :param current_doc_count: integer
                    example: 369
                :param key: string
                    example: 2023-06-10 00:00:00
                :param previous_doc_count: integer
                    example: 303
                :param previous_key: string
                    example: 2023-06-03 00:00:00
            }]
        }
        :raises ValueError: If query_type is not one of the accepted values.
        """
        uri = "/bar"
        applied_filters = {}
        
        VALID_QUERY_TYPE = {'BLOCK_QUERIES', 'NO_ANSWER_QUERIES', 'TOR_PROX_VPN_QUERIES', 'SUSPICIOUS_NAMESERVER_QUERIES'}
        if query_type.upper() not in VALID_QUERY_TYPE:
            raise ValueError("aggregates: query_type must be one of %r" % VALID_QUERY_TYPE)
            
        applied_filters.update({'query_type': query_type.lower()})
        
        return self.connection.post(uri, json.dumps({'applied_filters': applied_filters}))
        
    def histogram(self, query_type: str) -> Dict:
        """
        Query the histogram endpoint.
        
        This method sends a request to the histogram endpoint. 
        The endpoint generates histogram data for the specified query type. 
        Histograms are useful for providing a visual representation of the distribution 
        of numerical data. This can help to understand trends, patterns, and outliers 
        in the queried dataset. The two query types, QUERIES and BLOCKED_QUERIES, 
        represent total queries and queries that were blocked, respectively.
        
        :param query_type: The type of histogram query to perform. Accepted values are:
            QUERIES
            BLOCKED_QUERIES
        :return: A histogram response object with the following params.
        {
            :param query_type: The query type that the histogram is for.
            :param top_items: [{
                :param current_doc_count: integer
                    example: 237
                :param key: string
                    example: 2023-06-06 08:30:00
                :param previous_doc_count: integer
                    example: 0
            }]
        }
        :raises ValueError: If query_type is not one of the accepted values.
        """
        uri = "/histogram"
        applied_filters = {}
        
        VALID_QUERY_TYPE = {'QUERIES', 'BLOCKED_QUERIES'}
        if query_type.upper() not in VALID_QUERY_TYPE:
            raise ValueError("aggregates: query_type must be one of %r" % VALID_QUERY_TYPE)
            
        applied_filters.update({'query_type': query_type.lower()})
        
        return self.connection.post(uri, json.dumps({'applied_filters': applied_filters}))
        
    def report(self, report_id: str) -> Dict:
        """
        Query the report endpoint to get a specific report.

        This endpoint returns a specific report based on the provided report_id. The report is returned in PDF format.
        
        :param report_id: The ID (uuid) of the report.
        :return: A report in pdf format.
        
        """
        uri = "/report"
        applied_filters = {'report_id': report_id}
        
        return self.connection.post(uri, json.dumps({'applied_filters': applied_filters}), accept='application/pdf')
        
    def reports(self) -> Dict:
        """
        Query the reports endpoint to get a list of executive reports.

        This endpoint returns a list of executive reports. Each item in the list contains detailed information 
        about a particular report, including the client_id, datetime, datetime_end, datetime_start, and report_id.
        
        :return: An open containing a list of reports and the count.
        {
            :param reports: [{
                :param client_id: string
                    example: 6695ad37-811c-49c4-8975-c1263fb73aab
                :param datetime: string
                    example: 2023-02-23T04:06:20.070714Z
                :param datetime_end: string
                    example: March 10, 2023
                :param datetime_start: string
                    example: January 07, 2023
                :param report_id: string
                    example: 54bb5625-ec81-4bb7-a65d-dd8869a5353b
            }]
        }
        """
        uri = "/reports"
        
        return self.connection.post(uri, json.dumps({}))