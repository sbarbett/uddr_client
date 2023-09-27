import json, datetime, re
from typing import Dict, List, Optional
from ..response import Response
from ..connection import Connection
from .account import Account
from .decision import Decision

class APIClient:
    def __init__(self, connection: Connection):
        self.connection = connection
        
    def _is_valid_date(self, date: str) -> bool:
        """
        Validate if a string is in 'YYYY-MM-DDTHH:MM:SS.sssZ' or 'YYYY-MM-DD' format.

        :param date: The string to validate.
        :return: A boolean value. True if the string is a valid date, False otherwise.
        """
        formats = ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d")
        for date_format in formats:
            try:
                datetime.datetime.strptime(date, date_format)
                return True
            except ValueError:
                continue
        return False
        
    # Overview

    def aggregates(self, query_type: str, **kwargs) -> Response:
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

        response = self.connection.post(uri, json.dumps({'applied_filters': applied_filters}))
        return Response(response)

    def bar(self, query_type: str) -> Response:
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
        
        response = self.connection.post(uri, json.dumps({'applied_filters': applied_filters}))
        return Response(response)
        
    def histogram(self, query_type: str) -> Response:
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
        
        response = self.connection.post(uri, json.dumps({'applied_filters': applied_filters}))
        return Response(response)
        
    def summary(self, query_type: str) -> Response:
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

        response = self.connection.post(uri, json.dumps({'applied_filters': applied_filters}))
        return Response(response)
        
    # Reports
        
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
        
    def reports(self, datetime_start: Optional[str] = None, datetime_end: Optional[str] = None) -> Response:
        """
        Query the reports endpoint to get a list of executive reports.

        This endpoint returns a list of executive reports. Each item in the list contains detailed information 
        about a particular report, including the client_id, datetime, datetime_end, datetime_start, and report_id.
        
        :param datetime_start: The start date for the report in the format 'YYYY-MM-DDTHH:MM:SS.sssZ'
        :param datetime_end: The end date for the report in the format 'YYYY-MM-DDTHH:MM:SS.sssZ'
        :return: An object containing a list of reports and the count.
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
        data = {}

        if datetime_start:
            if self._is_valid_date(datetime_start):
                data['datetime_start'] = datetime_start
            else:
                raise ValueError(f"Invalid datetime_start format: {datetime_start}")

        if datetime_end:
            if self._is_valid_date(datetime_end):
                data['datetime_end'] = datetime_end
            else:
                raise ValueError(f"Invalid datetime_end format: {datetime_end}")

        response = self.connection.post(uri, json.dumps(data))
        return Response(response)

    # Logs

    def histogram_artifact(self, artifact: str, artifact_type: str, start_date: str, end_date: str, interval: str, **kwargs) -> Response:
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

        if not self._is_valid_date(start_date) or not self._is_valid_date(end_date):
            raise ValueError("histogram_artifact: start_date, end_date must be in the format 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SS.sssZ'")

        applied_filters.update({'start_date': start_date, 'end_date': end_date, 'interval': interval})

        if 'query_type' in kwargs:
            VALID_QUERY_TYPE = {'QUERIES', 'QUERIES_OVER_DAY', 'QUERIES_OVER_HOUR'}
            if kwargs['query_type'].upper() not in VALID_QUERY_TYPE:
                raise ValueError("histogram_artifact: query_type must be one of %r" % VALID_QUERY_TYPE)

            applied_filters.update({'query_type': kwargs['query_type'].lower()})

        response = self.connection.post(uri, json.dumps({'applied_filters': applied_filters}))
        return Response(response)

    def logs(self, applied_filters: List[Dict]) -> Response:
        """
        Query the logs endpoint.

        This method sends a request to the logs endpoint, which returns logs data based on the applied filters.
        
        NOTE: When you parse this into a CSV using the response handler it will return a list with 2 separate CSVs.

        :param applied_filters: A list of dictionaries, each representing a filter to be applied on the logs data.
            Each filter dictionary can include the following keys:
                - "exclude": (boolean) Flag to indicate if the filter value should be excluded.
                - "id": (string) The filter id, represents the field on which the filtering is applied. Accepted values are:
                    DOMAIN
                    DOMAIN_2TLD
                    DOMAIN_TLD
                    DOMAIN_AGE
                    QUERY_TYPE
                    RESPONSE_CODE
                    TTL
                    NAMESERVER
                    NAMESERVER_2TLD
                    NAMESERVER_TLD
                    NAMESERVER_IP
                    A_RECORD
                    AAAA_RECORD
                    C_NAME
                    C_NAME_2TLD
                    C_NAME_TLD
                    REGISTRAR
                    REPUTATION
                    DATETIME
                - "isRange": (boolean) Flag to indicate if the filter value is a range.
                - "partial": (boolean) Flag to indicate if the filter should do partial matching.
                - "rangeValue": (dictionary) If "isRange" is true, this dictionary with 'start' and 'end' keys represents the range value.
                - "value": (string) If "isRange" is false, this represents the filter value.

        :return: A logs response object.
        :raises ValueError: If 'id' is not a valid value or date format in 'rangeValue' is not 'YYYY-MM-DDTHH:MM:SS.sssZ'.
        """
        uri = "/logs"

        VALID_ID = {'DOMAIN', 'DOMAIN_2TLD', 'DOMAIN_TLD', 'DOMAIN_AGE', 'QUERY_TYPE', 'RESPONSE_CODE', 'TTL', 'NAMESERVER', 
                    'NAMESERVER_2TLD', 'NAMESERVER_TLD', 'NAMESERVER_IP', 'A_RECORD', 'AAAA_RECORD', 'C_NAME', 
                    'C_NAME_2TLD', 'C_NAME_TLD', 'REGISTRAR', 'REPUTATION', 'DATETIME'}

        # Validate and convert parameters to proper format
        for filter in applied_filters:
            filter['id'] = filter['id'].upper()
            if filter['id'] not in VALID_ID:
                raise ValueError(f"Invalid filter ID. Must be one of {VALID_ID}")

            if 'isRange' in filter and filter['isRange']:
                # Check date format for 'start' and 'end'
                for key in ('start', 'end'):
                    if not self._is_valid_date(filter['rangeValue'][key]):
                        raise ValueError(f"The '{key}' date in 'rangeValue' must be in 'YYYY-MM-DDTHH:MM:SS.sssZ' format.")
            filter['id'] = filter['id'].lower()

        response = self.connection.post(uri, json.dumps({'applied_filters': applied_filters}))
        return Response(response)
        
    # Passthrough
    
    def passthrough(self, applied_filters: List[Dict]) -> Response:
        """
        Query the passthrough endpoint.

        This method sends a request to the passthrough endpoint, which returns passthrough data based on the applied filters.
        
        :param applied_filters: A list of filters to be applied. Each filter is a dictionary with the following keys:
            - exclude: Flag to indicate if the filter value should be excluded (boolean).
            - id: The filter id (string), one of the following options:
                LAST_SEEN
                ARTIFACT
                HYAS_STATUS
                ALT_STATUS
                QUERY_COUNT
            - isRange: Flag to indicate if the filter value is a range (boolean).
            - partial: If the filter should do partial matching (boolean).
            - rangeValue: Dictionary with 'start' and 'end' keys representing the range start and end values (string in YYYY-MM-DDTHH:MM:SS format).
            - value: The filter value (string).
            
        :return: A dictionary containing the passthrough data.
        :raises ValueError: If 'id' is not a valid value or date format in 'rangeValue' is not 'YYYY-MM-DDTHH:MM:SS.sssZ'.
        """
        uri = "/passthrough"
        
        # validate that the filter ids are within the valid options
        valid_ids = ['LAST_SEEN', 'ARTIFACT', 'HYAS_STATUS', 'ALT_STATUS', 'QUERY_COUNT']
        for filter in applied_filters:
            if filter['id'].upper() not in valid_ids:
                raise ValueError(f"Invalid id in filter: {filter['id']}. Must be one of {valid_ids}")
                
            # if the filter is a range, validate the date strings
            if filter['isRange']:
                start = filter.get('rangeValue', {}).get('start')
                end = filter.get('rangeValue', {}).get('end')
                if start and not self._is_valid_date(start):
                    raise ValueError(f"Invalid start date in filter: {start}. Dates should be in the format 'YYYY-MM-DDTHH:MM:SS'.")
                if end and not self._is_valid_date(end):
                    raise ValueError(f"Invalid end date in filter: {end}. Dates should be in the format 'YYYY-MM-DDTHH:MM:SS'.")
                
        # make the request
        response = self.connection.post(uri, json.dumps({'applied_filters': applied_filters}))
        return Response(response)

    # Private APIs

    def category(self, domain: str) -> Response:
        """
        Query the category endpoint.

        This method sends a request to the category endpoint, which returns the category of a specified domain.

        :param domain: The domain to query.
        :return: A list containing the category data.
        :raises ValueError: If 'domain' is not a valid domain.
        """
        uri = "/category/v1"

        # validate that the domain is a legitimate domain name
        if not re.match(r'^(?=.{1,253}\.?$)(?:(?!-|[^.]+_)[A-Za-z0-9-]{1,63}(?<!-)\.?)+[A-Za-z]{2,6}$', domain):
            raise ValueError("The provided domain is not a valid domain name.")

        # make the request
        response = self.connection.post(uri, json.dumps({'domain': domain}), pvt=True)
        return response

    def account(self):
        """The account endpoint contains information about the user's account"""
        return Account(self.connection)

    def decision(self):
        """The decision engine endpoint"""
        return Decision(self.connection)