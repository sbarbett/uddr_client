import json
from ..response import Response

class Account:
    def __init__(self, connection):
        self.connection = connection
        self.service = '/account'

    def organization(self):
        return Organization(self.connection, self.service)

    def user(self):
        return User(self.connection, self.service)

class Organization:
    def __init__(self, connection, parent_service):
        self.connection = connection
        self.service = parent_service + '/organization'

    def settings(self):
        """Get the user's organization's settings"""
        response = self.connection.post(self.service + '/settings', data=json.dumps({}), pvt=True)
        return Response(response)

    def products(self):
        """Get the products associated with the user's organization"""
        response = self.connection.post(self.service + '/products', data=json.dumps({}), pvt=True)
        return Response(response)

    def packages(self):
        """Get the packages associated with the user's organization"""
        response = self.connection.post(self.service + '/packages', data=json.dumps({}), pvt=True)
        return Response(response)

class User:
    def __init__(self, connection, parent_service):
        self.connection = connection
        self.service = parent_service + '/user'

    def organizations(self):
        """Get the organization(s) associated with the user"""
        response = self.connection.post(self.service + '/organizations', data=json.dumps({}), pvt=True)
        return Response(response)