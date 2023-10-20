import uuid

import pymongo
from pymongo.results import InsertOneResult

from db import collection
from db.collectionnames import collection_templates, collection_users


class Template:

    def __init__(self, content: str = None) -> None:
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
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result


def get_template(template: Template):
    c = collection.get_collection_instance(collection_templates)
    result = c.find_one({"uuid": template.uuid})
    if result:
        content = result.get("content")
        if not content:
            content = []
        return content
    else:
        return []


def update_template(template: Template):
    c = collection.get_collection_instance(collection_templates)
    result = c.update_one({"uuid": template.uuid}, {"$set": {"content": template.content}})
    return result


def delete_template(template: Template):
    c = collection.get_collection_instance(collection_templates)
    result = c.delete_one({"uuid": template.uuid})
    return result


def get_all_template_by_page(page: int, page_size: int):
    c = collection.get_collection_instance(collection_templates)
    # Can be iterated by for loop
    result = c.find_all_by_page(page, page_size)
    if result:
        content = result.get("content")
        if not content:
            content = []
        return content
    else:
        return []
