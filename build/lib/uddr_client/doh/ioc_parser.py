import re
import ipaddress

class InvalidIOCError(Exception):
    pass

class IOCParser:
    def __init__(self, ioc: str):
        # Note: This logic is borrowed directly from the DDR-IOC-Checker
        # https://github.com/rybolov/DDR-IOC-Checker
        self.ioc = ioc.strip()  # Remove whitespace
        self.ioc = self.ioc.rstrip('.')  # For any lists that use DNS-style FQDNs that end with a dot.
        self.ioc = self.ioc.lower()  # Use all lower-case
        
        # Most CTI list domains as foo[.]com to keep you from clicking on them.
        self.ioc = re.sub('\[\.\]', '.', self.ioc)
        
        # Remove "http://", "https://", "hxxp://" and "hxxps://"
        self.ioc = re.sub('^h[tx]{2}ps*://', '', self.ioc)
        
        # Remove "/path/and/anything/else/here" and rely on regex being "greedy"
        self.ioc = re.sub('/.*$', '', self.ioc)
        
        if re.search('@', self.ioc):  # If the IOC is an email address
            self.ioc = re.sub('^.*@', '', self.ioc)

        # If it's an IP address
        try:
            ip = ipaddress.ip_address(self.ioc)

            if isinstance(ip, ipaddress.IPv4Address):  # If it's an IPv4 address
                self.ioc = '.'.join(self.ioc.split('.')[::-1]) + '.in-addr.arpa'

            elif isinstance(ip, ipaddress.IPv6Address):  # If it's an IPv6 address
                self.ioc = ip.exploded.replace(':', '')
                self.ioc = '.'.join(self.ioc[::-1]) + '.ip6.arpa'

        except ValueError:  # It's not an IP address
            # If it's not a valid hostname either
            if not re.match(r'^([a-z0-9]([a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}$', self.ioc):
                raise InvalidIOCError(f"'{self.ioc}' is not a valid IP address or hostname")

    def __str__(self) -> str:
        return self.ioc

    def __repr__(self) -> str:
        return self.__str__()