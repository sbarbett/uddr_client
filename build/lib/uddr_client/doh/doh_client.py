import json, socket, os
from decouple import config
from typing import List, Optional
from ..response import Response
from ..connection import Connection
from .ioc_parser import IOCParser


class DOHClient:
    class Lookup:
        def __init__(self, doh_client, ioc: str):
            self.doh_client = doh_client
            self.ioc = str(IOCParser(ioc))
            self.type, self.ioc = self._determine_type(self.ioc)
            self._cache = {} # Initialize a cache
            self.response = self._query()
            self.blocked = self._is_blocked()

        def _determine_type(self, ioc: str) -> tuple:
            if ioc.endswith('.in-addr.arpa') or ioc.endswith('.ip6.arpa'):
                return ('PTR', ioc)
            else:
                return (None, ioc)

        def _query(self, record_type: str = None) -> Response:
            if self.doh_client.client_id is not None:
                params = {'name': self.ioc}
                if record_type is None:
                    record_type = self.type
                if record_type is not None:
                    params['type'] = record_type
                return Response(self.doh_client.connection.get('/', client_id=self.doh_client.client_id, params=params))
            else:
                raise ValueError("No Client ID provided. Please set it via argument or call DOHClient.setup.")

        def _get_record(self, record_type: str) -> List[dict]:
            if record_type not in self._cache:
                self._cache[record_type] = self._query(record_type).get('Answer', [])
            return self._cache[record_type]

        def _is_blocked(self) -> bool:
            if self.doh_client.block_page_ip is not None:
                a_records = self._get_record('A')
                return any(record['data'] == self.doh_client.block_page_ip for record in a_records)
            return None

        def __str__(self) -> str:
            return str(self.response)

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
            if self.doh_client.block_page_enabled:
                if self.blocked is not None:
                    if self.blocked:
                        return {'blocked': True, 'domain': self.ioc, 'message': 'Blocked by UDDR'}
                    else:
                        return {'blocked': False, 'domain': self.ioc, 'message': 'Not blocked by UDDR'}
                else:
                    return {'blocked': None, 'domain': self.ioc, 'message': 'Block page IP not specified'}
            else:
                return {'blocked': None, 'domain': self.ioc, 'message': 'Block page is not enabled'}

        def answer(self) -> List[dict]:
            return self.response.get('Answer', [])

        def authority(self) -> List[dict]:
            return self.response.get('Authority', [])

    def __init__(self, connection: Connection, api_client, org_name: Optional[str] = None):
        self.api_client = api_client
        self.org_name = org_name or config('DEFAULT_ORG_NAME', default=None)
        self.client_id = self._get_client_id()
        self.connection = connection
        self._organization_settings = self._get_organization_settings()

    def __str__(self) -> str:
        return str(self.response)

    def __repr__(self) -> str:
        return self.__str__()

    def _get_client_id(self) -> str:
        resp = self.api_client.account().user().organizations()
        organizations = resp.get('organizations', [])

        if not organizations:
            raise ValueError("No organizations found for this user.")

        if len(organizations) == 1:
            client_id = organizations[0].get('client_id', None)
        else:
            if self.org_name is not None:
                for org in organizations:
                    if org.get('organization_name', None) == self.org_name:
                        client_id = org.get('client_id', None)
                        break
            else:
                print("Warning: Multiple organizations found for this user. Please specify one of the following organization names:")
                for org in organizations:
                    print(f"\t{org.get('organization_name')}")
                print("You can specify the organization name via the org_name keyword argument in the constructor or configure it in your environment using DOHClient.setup.")
                client_id = None

        return client_id

    @property
    def block_page_ip(self):
        return self._organization_settings.get('block_portal_ipv4', None)

    @property
    def block_page_enabled(self):
        return self._organization_settings.get('portal_enabled', None)

    def _get_organization_settings(self) -> dict:
        try:
            organizations = self.api_client.account().user().organizations().get('organizations', [])
            for org in organizations:
                if org.get('organization_name') == self.org_name:
                    settings = org.get('settings', {})
                    protect_settings = settings.get('protect_settings', {})
                    return {
                        'block_portal_ipv4': protect_settings.get('block_portal_ipv4', None),
                        'portal_enabled': protect_settings.get('portal_enabled', None)
                    }
        except Exception as e:
            print(f"An error occurred while trying to retrieve the organization settings: {e}")
        return {}

    def lookup(self, ioc: str):
        return self.Lookup(self, ioc)

    def setup(self, **kwargs):
        """
        This method stores the user's default organization name in their .env file for later use.

        :param org_name: (Optional) The user's organization name.
        """
        env_var_key = 'DEFAULT_ORG_NAME'
        org_name = kwargs.get('org_name')

        # Get the list of organizations
        try:
            resp = self.api_client.account().user().organizations()
            organizations = resp.get('organizations', [])
            organization_names = [org.get('organization_name') for org in organizations if org.get('organization_name')]
        except Exception as e:
            print(f"Error fetching the list of organizations: {e}")
            return

        # If an .env file doesn't exist, create it
        if not os.path.exists('.env'):
            open('.env', 'a').close()

        # Read the existing content of the .env file
        with open('.env', 'r') as f:
            lines = f.readlines()

        # Check if the env_var_key already exists in the file
        env_var_exists = any(line.startswith(env_var_key + '=') for line in lines)

        if org_name is None or org_name not in organization_names:
            if env_var_exists:
                existing_value = config(env_var_key)
                print(f"{env_var_key} is already set in .env file as {existing_value}.")

            while org_name not in organization_names:
                if organization_names:
                    print("Please enter a valid organization name from the list below:")
                    print("\n".join(organization_names))
                org_name = input(f'Enter a value for {env_var_key}: ')

        # If the variable already exists, update its value. Otherwise, append it.
        if env_var_exists:
            lines = [line if not line.startswith(env_var_key + '=') else f'{env_var_key}={org_name}\n' for line in
                     lines]
        else:
            lines.append(f'{env_var_key}={org_name}\n')

        # Write the modified content back to the .env file
        with open('.env', 'w') as f:
            f.writelines(lines)