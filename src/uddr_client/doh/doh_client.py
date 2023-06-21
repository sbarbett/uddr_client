from ..response import Response
from ..connection import Connection

class DOHClient:
    def __init__(self, connection: Connection, ioc: str):
        self.connection = connection
        self.ioc = ioc
        self.response = Response(connection.get('/', doh=True, params={'name': ioc}))
        
    def __str__(self) -> str:
        return str(self.response)

    def __repr__(self) -> str:
        return str(self.__str__())