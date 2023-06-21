from ..connection import Connection

class DOHClient:
    def __init__(self, connection: Connection, ioc: str):
        self.connection = connection
        self.ioc = ioc
        return self.connection.get('/', doh=True, params={'name', ioc})