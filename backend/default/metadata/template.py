import uuid

import pymongo
from pymongo.results import InsertOneResult

user_collection_name = "users"

template_collection_name = "templates"


class Template:

    def __init__(self, content: str = None) -> None:
        self.uuid = uuid.uuid4().hex
        self.content = content


def insert_template(template: Template) -> InsertOneResult:
    c = connection.get_collection(user_collection_name)

    template_document = {
        "uuid": template.uuid,
        "content": template.content,
    }

    try:
        c = connection.get_collection(template_collection_name)
        result = c.insert_one(template_document)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result


def get_template(template: Template):
    c = connection.get_collection(template_collection_name)
    result = c.find_one({"uuid": template.uuid})
    if result:
        content = result.get("content")
        if not content:
            content = []
        return content
    else:
        return []


def update_template(template: Template):
    c = connection.get_collection(template_collection_name)
    result = c.update_one({"uuid": template.uuid}, {"$set": {"content": template.content}})
    return result


def delete_template(template: Template):
    c = connection.get_collection(template_collection_name)
    result = c.delete_one({"uuid": template.uuid})
    return result


def get_all_template_by_page(page: int, page_size: int):
    c = connection.get_collection(template_collection_name)
    result = c.find().skip((page - 1) * page_size).limit(page_size)
    if result:
        content = result.get("content")
        if not content:
            content = []
        return content
    else:
        return []
