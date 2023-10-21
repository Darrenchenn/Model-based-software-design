# storage functions of archives.


import uuid
import pymongo
from pymongo.results import InsertOneResult
from backend.default.db import collection, collectionnames


class Archive:

    # content: map<object, object> (Product, Audit)
    def __init__(self, content: dict[object, object] = {}) -> None:
        self.uuid = uuid.uuid4().hex
        self.content = content

def insert_archive(archive: Archive) -> InsertOneResult:
    c = collection.get_collection_instance(collectionnames.collection_archives)

    archive_document = {
        "uuid": archive.uuid,
        "content": archive.content,
    }

    try:
        result = c.insert_one(archive_document)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result

def get_archive_by_uuid(uuid:str):
    archive_document = {
        "uuid": uuid,
    }
    c = collection.get_collection_instance(collectionnames.collection_archives)
    try:
        result = c.find_one(archive_document)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result
    
def get_archive_content_by_uuid(uuid:str):
    archive_document = {
        "uuid": uuid,
    }
    c = collection.get_collection_instance(collectionnames.collection_archives)
    try:
        result = c.find_one(archive_document)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result.get("content")
    
def update_archive(new_archive:Archive):
    c = collection.get_collection_instance(collectionnames.collection_archives)
    original_archive = c.find_one({"uuid": new_archive.uuid})
    if not new_archive.content:
        new_archive.content = original_archive.get("content")
    result = c.update_one({"uuid": new_archive.uuid}, {"$set": {"content": new_archive.content}})
    return result

def delete_archive_by_uuid(uuid: str):
    c = collection.get_collection_instance(collectionnames.collection_archives)
    result = c.delete_one({"uuid": uuid})
    return result
