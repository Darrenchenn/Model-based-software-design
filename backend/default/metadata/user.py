import pymongo
import uuid

from pymongo.results import InsertOneResult

from default.db import connection

user_collection_name = "users"

class user:
    """A user of the application.
    Parameters:
    username (str): The user's username. This is the user's unique identifier.
    password (str): The user's password. Could be None if you want to search for a user.
    user_type (str): The user's type. Could be None.
    contact_info (ContactInfo): The user's contact information. Could be None."""

    def __init__(self, username, password=None, user_type=None, contact_info=None):
        self.uuid = uuid.uuid4().hex
        self.username = username
        self.password = password
        self.user_type = user_type
        self.contact_info = contact_info
    
    def __str__(self):
        return "User: %s" %(self.username)
    
    def __repr__(self):
        return "User: %s" %(self.username)
    
    def __eq__(self, other):
        return self.username == other.username
    
    def __hash__(self):
        return hash(self.uuid)
    
    def insertUser(self, password=None, wechat_id=None, email=None) -> InsertOneResult:
        c = connection.get_collection(user_collection_name)

        contact_info = {
            "wechat_id": wechat_id,
            "email": email
        }
        
        user_document = {
            "uuid": self.uuid,
            "username": self.username,
            "password": self.password,
            "contact_info": contact_info,
            "user_type": self.user_type
        }
        
        try:
            result = c.insert_one(user_document)
        except pymongo.errors.OperationFailure:
            print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
        else:
            return result
        

    def findUser(self):
        c = connection.get_collection(user_collection_name)

        user_document = {
            "username": self.username
        }
        try:
            result = c.find_one(user_document)
        except pymongo.errors.OperationFailure:
            print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
        else:
            if result:
                return result
            else:
                return None
            
    def updateUser(self, password=None, wechat_id=None, email=None):
        c = connection.get_collection(user_collection_name)

        user_document = {
            "username": self.username
        }

        result = c.find_one(user_document)

        print(result.keys())

        if(password is None):
            password = result["password"]

        contact_info = result.get("contact_info", {})

        if wechat_id is None:
            wechat_id = contact_info.get("wechat_id")

        if email is None:
            email = contact_info.get("email")
        
        contact_info = {
            "wechat_id": wechat_id,
            "email": email
        }
        
        new_values = {
            "$set": {
                "password": password,
                "contact_info": contact_info
            }
        }
        
        try:
            result = c.update_one(user_document, new_values)
        except pymongo.errors.OperationFailure:
            print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
        else:
            print("Successfully updated user with username: %s" %(self.username))
            return result
            
    def deleteUser(self):
        c = connection.get_collection(user_collection_name)

        user_document = {
            "username": self.username
        }

        try:
            result = c.delete_one(user_document)
        except pymongo.errors.OperationFailure:
            print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
        else:
            return result