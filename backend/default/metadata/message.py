import uuid

import pymongo
from pymongo.results import InsertOneResult
from backend.default.db import collection
from backend.default.db import collectionnames

class Message:
    """Message metadata class.
    Parameters:
    uuid (str): The message's unique identifier.
    content (str): The message's content.
    email (str): The message's email.
    wechat (str): The message's wechat."""

    def __init__(self, username:str = None, content: str = None, email: str = None, wechat: str = None) -> None:
        self.uuid = uuid.uuid4().hex
        self.username = username
        self.content = content
        self.email = email
        self.wechat = wechat


def insert_message(message: Message) -> InsertOneResult:
    c = collection.get_collection_instance(collectionnames.collection_messages)

    message_document = {
        "uuid": message.uuid,
        "content": message.content,
        "email": message.email,
        "wechat": message.wechat,
    }

    try:
        result = c.insert_one(message_document)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result
    
def get_message_by_uuid(uuid:str):
    message_document = {
        "uuid": uuid,
    }
    c = collection.get_collection_instance(collectionnames.collection_messages)
    try:
        result = c.find_one(message_document)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result
    
def get_message_by_username_and_page(username:str, page:int, page_size:int):
    message_document = {
        "username": username,
    }
    c = collection.get_collection_instance(collectionnames.collection_messages)
    try:
        # Can be iterated by for loop
        result = c.find_all_by_page(message_document, page, page_size)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result

