from ..connection import Connection

class DOHClient:
    def __init__(self, connection: Connection, ioc: str):
        self.connection = connection
        self.ioc = ioc