import uuid

import pymongo
from pymongo.results import InsertOneResult

from default.db import connection

user_collection_name = "users"

class ContactInfo:
    """The contact information of a user.
    Parameters:
    wechat_id (str): The user's WeChat ID.
    email (str): The user's email address."""
    def __init__(self, wechat_id:str=None, email:str=None):
        self.wechat_id = wechat_id
        self.email = email

class User:
    """A user of the application.
    Parameters:
    username (str): The user's username. This is the user's unique identifier.
    password (str): The user's password. Could be None if you want to search for a user.
    user_type (str): The user's type. Could be None.
    contact_info (ContactInfo): The user's contact information. Could be None."""

    def __init__(self, username, password=None, user_type=None, contact_info:ContactInfo=None):
        self.uuid = uuid.uuid4().hex
        self.username = username
        self.password = password
        self.user_type = user_type
        self.contact_info = contact_info

    def __str__(self):
        return "User: %s" % self.username

    def __repr__(self):
        return "User: %s" % self.username

    def __eq__(self, other):
        return self.username == other.username

    def __hash__(self):
        return hash(self.uuid)


def insert_user(user:User) -> InsertOneResult:
    c = connection.get_collection(user_collection_name)

    user_document = {
        "uuid": user.uuid,
        "username": user.username,
        "password": user.password,
        "contact_info": user.contact_info,
        "user_type": user.user_type
    }

    try:
        result = c.insert_one(user_document)
    except pymongo.errors.OperationFailure:
        print(
            "An authentication error was received. Are you sure your database user is authorized to perform write "
            "operations?")
    else:
        return result

def find_user(user:User):
    c = connection.get_collection(user_collection_name)

    user_document = {
        "username": user.username
    }

    try:
        result = c.find_one(user_document)
    except pymongo.errors.OperationFailure:
        print(
            "An authentication error was received. Are you sure your database user is authorized to perform write "
            "operations?")
    else:
        if result:
            return result
        else:
            return None

def update_user(user:User):
    c = connection.get_collection(user_collection_name)

    user_document = {
        "username": user.username
    }
    result = c.find_one(user_document)

    print(result.keys())

    if user.password is None:
        password = result.get("password")
    if user.user_type is None:
        user_type = result.get("user_type")

    contact_info = result.get("contact_info", {})
    if user.contact_info.wechat_id is None:
        wechat_id = contact_info.get("wechat_id")
    if user.contact_info.email is None:
        email = contact_info.get("email")

    contact_info = {
        "wechat_id": wechat_id,
        "email": email
    }

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
        print(
            "An authentication error was received. Are you sure your database user is authorized to perform write "
            "operations?")
    else:
        print("Successfully updated user with username: %s" % user.username)
        return result

def delete_user(user:User):
    c = connection.get_collection(user_collection_name)
    user_document = {
        "username": user.username
    }
    try:
        result = c.delete_one(user_document)
    except pymongo.errors.OperationFailure:
        print(
            "An authentication error was received. Are you sure your database user is authorized to perform write "
            "operations?")
    else:
        return result
