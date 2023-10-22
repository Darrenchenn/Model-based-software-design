# storage functions of archives.


import uuid

import pymongo
from pymongo.results import InsertOneResult

from Backend.default.db import collection, collectionnames
from Backend.default.metadata.audit import Audit

from Backend.default.common.error import Error


class Archive:

    # content: map<string, object> (product_uuid, Audit)
    def __init__(self, content: dict = {}) -> None:
        self.uuid = uuid.uuid4().hex
        self.content = content


def insert_archive(archive: Archive) -> InsertOneResult:
    c = collection.get_collection_instance(collectionnames.collection_archives)

    for key, value in archive.content.items():
        if isinstance(value, Audit):
            archive.content[key] = value.to_dict()

    archive_document = {
        "uuid": archive.uuid,
        "content": archive.content,
    }

    try:
        result = c.insert_one(archive_document)
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def get_archive_by_uuid(uuid: str):
    archive_document = {
        "uuid": uuid,
    }
    c = collection.get_collection_instance(collectionnames.collection_archives)
    try:
        result = c.find_one(archive_document)
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def get_archive_content_by_uuid(uuid: str):
    archive_document = {
        "uuid": uuid,
    }
    c = collection.get_collection_instance(collectionnames.collection_archives)
    try:
        result = c.find_one(archive_document)
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error.get("content")


def update_archive(new_archive: Archive):
    c = collection.get_collection_instance(collectionnames.collection_archives)
    try:
        original_archive = c.find_one({"uuid": new_archive.uuid})
        if not new_archive.content:
            new_archive.content = original_archive.get("content")
        result = c.update_one({"uuid": new_archive.uuid}, {"$set": {"content": new_archive.content}})
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def delete_archive_by_uuid(uuid: str):
    c = collection.get_collection_instance(collectionnames.collection_archives)
    try:
        result = c.delete_one({"uuid": uuid})
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error
