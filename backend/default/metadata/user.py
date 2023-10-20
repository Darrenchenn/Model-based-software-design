import uuid

import pymongo
from pymongo.results import InsertOneResult
from pymongo.results import UpdateResult
from db import collection
from db.collectionnames import collection_users

class ContactInfo:
    """The contact information of a user.
    Parameters:
    wechat_id (str): The user's WeChat ID.
    email (str): The user's email."""
    def __init__(self, wechat_id:str=None, email:str=None):
        self.wechat_id = wechat_id
        self.email = email

class User:
    """A user of the application.
    Parameters:
    username (str): The user's username. This is the user's unique identifier.
    password (str): The user's password. Could be None if you want to search for a user.
    user_type (str): The user's type. Could be None if you want to search for a user.
    contact_info (ContactInfo): The user's contact information. Could be None if you want to search for a user."""

    def __init__(self, username, password=None, user_type=None, contact_info:ContactInfo=None):
        self.uuid = uuid.uuid4().hex
        self.username = username
        self.password = password
        self.user_type = user_type
        self.contact_info = contact_info

def insert_user(user:User)->InsertOneResult:
    c = collection.get_collection_instance(collection_users)

    # Username is the unique identifier of a user.
    result = c.find_one({"username": user.username})
    if result:
        return None

    user_document = {
        "uuid": user.uuid,
        "username": user.username,
        "password": user.password,
        "user_type": user.user_type,
        "contact_info": {
            "wechat_id": user.contact_info.wechat_id,
            "email": user.contact_info.email
        }
    }

    try:
        result = c.insert_one(user_document)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result
    
def get_user_by_username(username:str):
    user_document = {
        "username": username,
    }
    c = collection.get_collection_instance(collection_users)
    try:
        result = c.find_one(user_document)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result
    
def get_user_by_uuid(uuid:str):
    user_document = {
        "uuid": uuid,
    }
    c = collection.get_collection_instance(collection_users)
    try:
        result = c.find_one(user_document)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result

def update_user(user:User) -> UpdateResult:
    user_document = {
        "username": user.username,
    }
    c = collection.get_collection_instance(collection_users)
    result = c.find_one(user_document)
    if result:
        password = result.get("password")
        user_type = result.get("user_type")
        contact_info = result.get("contact_info")
    else:
        return None
    new_values = {
        "$set": {
            "password": password,
            "user_type": user_type,
            "contact_info": contact_info
        }
    }
    try:
        result = c.update_one(user_document, new_values)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result


