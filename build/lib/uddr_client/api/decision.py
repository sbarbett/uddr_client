import json
from ..response import Response

class Decision:
    def __init__(self, connection):
        self.connection = connection
        self.service = '/decision'

    def baseline(self):
        return Baseline(self.connection, self.service)

class Baseline:
    def __init__(self, connection, parent_service):
        self.connection = connection
        self.service = parent_service + '/baseline'

    def countries(self):
        """Get the baseline countries. The object will contain full country names and their ISO codes."""
        response = self.connection.get(self.service + '/countries', pvt=True)
        return Response(response)