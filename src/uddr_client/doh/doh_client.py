import json, socket
from typing import List, Optional
from ..response import Response
from ..connection import Connection
from .ioc_parser import IOCParser

class DOHClient:
    def __init__(self, connection: Connection, ioc: str):
        self._cache = {}  # Initialize a cache
        self.connection = connection
        self.ioc = str(IOCParser(ioc))
        self.type, self.ioc = self._determine_type(self.ioc)
        self.response = self._query()
        self.blocked = self._is_blocked()

    def __str__(self) -> str:
        return str(self.response)

    def __repr__(self) -> str:
        return self.__str__()
        
    def _determine_type(self, ioc: str) -> tuple:
        if ioc.endswith('.in-addr.arpa') or ioc.endswith('.ip6.arpa'):
            return ('PTR', ioc)
        else:
            return (None, ioc)

    def _query(self, record_type: str = None) -> Response:
        params = {'name': self.ioc}
        if record_type is None:
            record_type = self.type
        if record_type is not None:
            params['type'] = record_type
        return Response(self.connection.get('/', doh=True, params=params))

    def _get_record(self, record_type: str) -> List[dict]:
        if record_type not in self._cache:  # If the record is not in the cache
            self._cache[record_type] = self._query(record_type=record_type).get('Answer', [])  # Query it and cache the result
        return self._cache[record_type]  # Return the cached result
        
    def _is_blocked(self) -> bool:
        a_records = self._get_record('A')
        for record in a_records:
            if record['data'] == '20.13.128.62':
                return True
        return False

    @property
    def A(self) -> List[dict]:
        return self._get_record('A')
        
    @property
    def AAAA(self) -> List[dict]:
        return self._get_record('AAAA')
        
    @property
    def CNAME(self) -> List[dict]:
        return self._get_record('CNAME')
        
    @property
    def MX(self) -> List[dict]:
        return self._get_record('MX')

    @property
    def NS(self) -> List[dict]:
        return self._get_record('NS')
        
    @property
    def SOA(self) -> List[dict]:
        return self._get_record('SOA')
        
    @property
    def SRV(self) -> List[dict]:
        return self._get_record('SRV')
        
    @property
    def TXT(self) -> List[dict]:
        return self._get_record('TXT')
        
    @property
    def CAA(self) -> List[dict]:
        return self._get_record('CAA')
        
    @property
    def DS(self) -> List[dict]:
        return self._get_record('DS')
        
    @property
    def DNSKEY(self) -> List[dict]:
        return self._get_record('DNSKEY')
        
    def status(self) -> dict:
        status = self.response.get('Status')
        reason = {'rcode': status}
        if status == 0:
            reason.update({'message': 'NOERROR', 'desc': 'DNS Query received by server'})
        elif status == 1:
            reason.update({'message': 'FORMERR', 'desc': 'DNS Query Format Error'})
        elif status == 2:
            reason.update({'message': 'SERVFAIL', 'desc': 'Server failed to complete the DNS request'})
        elif status == 3:
            reason.update({'message': 'NXDOMAIN', 'desc': 'Domain name does not exist'})
        elif status == 4:
            reason.update({'message': 'NOTIMP', 'desc': 'Function not implemented'})
        elif status == 5:
            reason.update({'message': 'REFUSED', 'desc': 'The server refused to answer for the query'})
        elif status == 6:
            reason.update({'message': 'YXDOMAIN', 'desc': 'Name that should not exist, does exist'})
        elif status == 7:
            reason.update({'message': 'XRRSET', 'desc': 'RRset that should not exist, does exist'})
        elif status == 8:
            reason.update({'message': 'NOTAUTH', 'desc': 'Server not authoritative for the zone'})
        elif status == 9:
            reason.update({'message': 'NOTZONE', 'desc': 'Name not in zone'})
        else:
            reason.update({'message': 'UNKNOWN', 'desc': 'Unknown/unexpected status'})
        
        return reason
        
    def block_info(self) -> dict:
        if self.blocked:
            return {'blocked': True, 'domain': self.ioc, 'message': 'Blocked by UDDR'}
        else:
            return {'blocked': False, 'domain': self.ioc, 'message': 'Not blocked by UDDR'}
            
    def answer(self) -> List[dict]:
        return self.response.get('Answer', [])
        
    def authority(self) -> List[dict]:
        return self.response.get('Authority', [])