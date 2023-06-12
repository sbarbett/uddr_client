from .connection import Connection
import json, re
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
        
    def summary(self, query_type: str) -> Dict:
        """
        Query the summary endpoint to get request summaries.

        This endpoint returns a summary of requests based on the provided query type. The summary contains 
        the total_count, query_type and day_count.

        :param query_type: The type of summary query to perform. Accepted values are:
            'TOTAL'
            'BLOCKED'
            'INDICATORS'
        :return: A summary response object.
        {
            :param day_count: integer
                example: 1
            :param query_type: string
                example: 'BLOCKED'
            :param total_count: integer
                example: 0
        }
        :raises ValueError: If query_type is not one of the accepted values.
        """
        uri = "/summary"
        applied_filters = {}

        VALID_QUERY_TYPE = {'TOTAL', 'BLOCKED', 'INDICATORS'}
        if query_type.upper() not in VALID_QUERY_TYPE:
            raise ValueError("summary: query_type must be one of %r" % VALID_QUERY_TYPE)
        
        applied_filters.update({'query_type': query_type.upper()})

        return self.connection.post(uri, json.dumps({'applied_filters': applied_filters}))

    def histogram_artifact(self, artifact: str, artifact_type: str, start_date: str, end_date: str, interval: str, **kwargs) -> Dict:
        """
        Query the histogram/artifact endpoint.

        This method sends a request to the histogram/artifact endpoint.
        The endpoint provides histogram data for the pop out panel timeline chart.

        :param artifact: The artifact
        :param artifact_type: The artifact type. Accepted values are:
            DOMAIN.KEYWORD
            DOMAIN_2TLD.KEYWORD
            NAMESERVER_TLD.KEYWORD
            NAMESERVER.KEYWORD
            NAMESERVER_IP.KEYWORD
            RESPONSE.A.KEYWORD
            RESPONSE.AAAA.KEYWORD
            RESPONSE.CNAME.KEYWORD
            RESPONSE.CNAME_2TLD.KEYWORD
        :param start_date: The start window in format YYYY-MM-DD
        :param end_date: The end window in format YYYY-MM-DD
        :param interval: The interval for the aggregate
        :param query_type: (Optional) The type of query. Accepted values are:
            QUERIES
            QUERIES_OVER_DAY
            QUERIES_OVER_HOUR
        :return: A histogram artifact response.
        :raises ValueError: If artifact_type, query_type are not one of the accepted values or if start_date, end_date are not in the correct format.
        """

        uri = "/histogram/artifact"
        applied_filters = {'artifact': artifact}

        VALID_ARTIFACT_TYPE = {'DOMAIN.KEYWORD', 'DOMAIN_2TLD.KEYWORD', 'NAMESERVER_TLD.KEYWORD', 'NAMESERVER.KEYWORD', 
                               'NAMESERVER_IP.KEYWORD', 'RESPONSE.A.KEYWORD', 'RESPONSE.AAAA.KEYWORD', 'RESPONSE.CNAME.KEYWORD', 'RESPONSE.CNAME_2TLD.KEYWORD'}
        if artifact_type.upper() not in VALID_ARTIFACT_TYPE:
            raise ValueError("histogram_artifact: artifact_type must be one of %r" % VALID_ARTIFACT_TYPE)

        applied_filters.update({'artifact_type': artifact_type.lower()})

        if not re.fullmatch("\d{4}-\d{2}-\d{2}", start_date) or not re.fullmatch("\d{4}-\d{2}-\d{2}", end_date):
            raise ValueError("histogram_artifact: start_date, end_date must be in the format 'YYYY-MM-DD'")

        applied_filters.update({'start_date': start_date, 'end_date': end_date, 'interval': interval})

        if 'query_type' in kwargs:
            VALID_QUERY_TYPE = {'QUERIES', 'QUERIES_OVER_DAY', 'QUERIES_OVER_HOUR'}
            if kwargs['query_type'].upper() not in VALID_QUERY_TYPE:
                raise ValueError("histogram_artifact: query_type must be one of %r" % VALID_QUERY_TYPE)

            applied_filters.update({'query_type': kwargs['query_type'].lower()})

        return self.connection.post(uri, json.dumps({'applied_filters': applied_filters}))
