from default.db import connection


class user:
    def __init__(self,uuid):
        self.uuid = uuid

    def create_user(self,connection_name,username,password,email=None):
        c = connection.get_connection(connection_name)
        #let's create two documents
        user = {
            "user_uuid": "RR000123456",
            "user_name" : "user1",
            "email":""
        }

        return c.insert_one(user)