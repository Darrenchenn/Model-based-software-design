import json
import uuid

import pymongo
from pymongo.results import InsertOneResult

from Backend.default.db import collection
from Backend.default.db.collectionnames import collection_messages
from Backend.default.common.error import Error


class Message:
    """Message metadata class.
    Parameters:
    uuid (str): The message's unique identifier.
    content (str): The message's content.
    email (str): The message's email.
    wechat (str): The message's wechat."""

    def __init__(self, username: str = None, content: str = None, email: str = None, wechat: str = None) -> None:
        self.uuid = uuid.uuid4().hex
        self.username = username
        self.content = content
        self.email = email
        self.wechat = wechat

    def to_dict(self) -> dict:
        return {
            "uuid": self.uuid,
            "username": self.username,
            "content": self.content,
            "email": self.email,
            "wechat": self.wechat,
        }
    
    def from_result_to_message(self, result):
        self.uuid = result.get("uuid", uuid.uuid4().hex)
        self.username = result.get("username", "")
        self.content = result.get("content", "")
        self.email = result.get("email", "")
        self.wechat = result.get("wechat", "")
        return self


def insert_message(json_body: dict) -> str:
    if not json_body.get("uuid"):
        return Error("uuid is required")
    if not json_body.get("content"):
        return Error("content is required")
    if not json_body.get("email") and not json_body.get("wechat"):
        return Error("email or wechat is required")
    c = collection.get_collection_instance(collection_messages)

    message = Message().from_result_to_message(json_body).to_dict()

    try:
        c.insert_one(message)
        return_uuid = json_body.get("uuid")
        return json.dumps(return_uuid)
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def get_message_by_uuid(uuid: str) -> str:
    message_document = {
        "uuid": uuid,
    }
    c = collection.get_collection_instance(collection_messages)
    try:
        result = c.find_one(message_document)
        message = Message().from_result_to_message(result).to_dict()
        return json.dumps(message)
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def get_message_by_username_and_page(username: str, page: int = 0, page_size: int = 10) -> str:
    message_document = {
        "username": username,
    }
    c = collection.get_collection_instance(collection_messages)
    try:
        # Can be iterated by for loop
        result = c.find_by_page(message_document, page, page_size)
        messages = []
        for message in result:
            message = Message().from_result_to_message(message).to_dict()
            messages.append(message)
        return json.dumps(messages)
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error
