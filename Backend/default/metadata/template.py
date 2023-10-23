import uuid

import pymongo
from pymongo.results import InsertOneResult

from default.db import collection
from default.db.collectionnames import collection_templates

from default.common.error import Error


class Template:

    def __init__(self, content: list = []) -> None:
        self.uuid = uuid.uuid4().hex
        self.content = content


def insert_template(template: Template) -> InsertOneResult:
    c = collection.get_collection_instance(collection_templates)

    template_document = {
        "uuid": template.uuid,
        "content": template.content,
    }

    try:
        result = c.insert_one(template_document)
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def get_template(template: Template):
    c = collection.get_collection_instance(collection_templates)
    try:
        result = c.find_one({"uuid": template.uuid})
        if result:
            content = result.get("content")
            if not content:
                content = []
            return content
        else:
            return []
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error



def update_template(template: Template):
    c = collection.get_collection_instance(collection_templates)
    try:
        result = c.update_one({"uuid": template.uuid}, {"$set": {"content": template.content}})
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def delete_template_by_uuid(uuid: str):
    c = collection.get_collection_instance(collection_templates)
    try:
        result = c.delete_one({"uuid": uuid})
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def get_all_template_by_page(page: int, page_size: int):
    c = collection.get_collection_instance(collection_templates)
    try:
    # Can be iterated by for loop
        result = c.find_by_page({}, page, page_size)
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def get_content_by_uuid(uuid: str):
    c = collection.get_collection_instance(collection_templates)
    try:
        result = c.find_one({"uuid": uuid})
        if result:
            content = result.get("content")
            if not content:
                content = []
            return content
        else:
            return []
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error