import re

class IOCParser:
    def __init__(self, ioc: str):
        # Note: This code is borrowed directly from the DDR-IOC-Checker
        # https://github.com/rybolov/DDR-IOC-Checker
        self.ioc = ioc.strip()  # Remove whitespace
        self.ioc = self.ioc.rstrip('.')  # For any lists that use DNS-style FQDNs that end with a dot.
        self.ioc = self.ioc.lower()  # Use all lower-case
        
        # Most CTI list domains as foo[.]com to keep you from clicking on them.
        self.ioc = re.sub('\[\.\]', '.', self.ioc)
        
        # Remove "http://", "https://" "hxxp://" and "hxxps://"
        self.ioc = re.sub('^h[tx]{2}ps*://', '', self.ioc)
        
        # Remove "/path/and/anything/else/here" and rely on regex being "greedy"
        self.ioc = re.sub('/.*$', '', self.ioc)
        
        if re.search('@', self.ioc):
            self.ioc = re.sub('^.*@', '', self.ioc)
            
    def __str__(self) -> str:
        return self.ioc

    def __repr__(self) -> str:
        return self.__str__()