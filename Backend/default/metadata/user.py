import uuid

import pymongo
from pymongo.results import InsertOneResult
from pymongo.results import UpdateResult

from Backend.default.db import collection
from Backend.default.db.collectionnames import collection_users

from Backend.default.common.error import Error


class ContactInfo:
    """The contact information of a user.
    Parameters:
    wechat_id (str): The user's WeChat ID.
    email (str): The user's email."""

    def __init__(self, wechat_id: str = None, email: str = None):
        self.wechat_id = wechat_id
        self.email = email

    def to_dict(self):
        return {
            "wechat_id": self.wechat_id,
            "email": self.email
        }


class User:
    """A user of the application.
    Parameters:
    uuid (str): The user's unique identifier.
    username (str): The user's username. This is the user's unique identifier.
    password (str): The user's password. Could be None if you want to search for a user.
    user_type (str): The user's type. Could be None if you want to search for a user.
    contact_info (ContactInfo): The user's contact information. Could be None if you want to search for a user."""

    def __init__(self, username, password=None, user_type=None, contact_info: ContactInfo = None):
        self.uuid = uuid.uuid4().hex
        self.username = username
        self.password = password
        self.user_type = user_type
        if contact_info is None:
            self.contact_info = ContactInfo().to_dict()


def insert_user(user: User) -> InsertOneResult:
    c = collection.get_collection_instance(collection_users)

    # Username is the unique identifier of a user.
    result = c.find_one({"username": user.username})
    if result:
        return None

    # Could not insert a user without a password.
    if user.password is None:
        return None

    user_document = {
        "uuid": user.uuid,
        "username": user.username,
        "password": user.password,
        "user_type": user.user_type,
        "contact_info": user.contact_info
    }

    try:
        result = c.insert_one(user_document)
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def get_user_by_username(username: str):
    user_document = {
        "username": username,
    }
    c = collection.get_collection_instance(collection_users)
    try:
        result = c.find_one(user_document)
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def get_user_by_uuid(uuid: str):
    user_document = {
        "uuid": uuid,
    }
    c = collection.get_collection_instance(collection_users)
    try:
        result = c.find_one(user_document)
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def update_user(user: User) -> UpdateResult:
    c = collection.get_collection_instance(collection_users)

    user_document = {
        "username": user.username,
    }
    original_user = c.find_one(user_document)
    if user.password is None:
        user.password = original_user.get("password")
    if user.user_type is None:
        user.user_type = original_user.get("user_type")
    if user.contact_info is ContactInfo:
        user.contact_info = original_user.get("contact_info")
    new_user_document = {
        "$set": {
            "password": user.password,
            "user_type": user.user_type,
            "contact_info": user.contact_info
        }
    }
    try:
        result = c.update_one(user_document, new_user_document)
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def delete_user_by_username(username: str):
    user_document = {
        "username": username,
    }
    c = collection.get_collection_instance(collection_users)
    try:
        result = c.delete_one(user_document)
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def delete_user_by_uuid(uuid: str):
    user_document = {
        "uuid": uuid,
    }
    c = collection.get_collection_instance(collection_users)
    try:
        result = c.delete_one(user_document)
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error
