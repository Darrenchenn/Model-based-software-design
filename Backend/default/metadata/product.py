# products storage functions
import uuid

import pymongo
from pymongo.results import InsertOneResult, DeleteResult

from Backend.default.db import collection
from Backend.default.db.collectionnames import collection_products

from Backend.default.common.error import Error


class Product:

    def __init__(self, creator: str, responsible_supervisor: str = None, content: str = None) -> None:
        self.uuid = uuid.uuid4().hex
        self.creator = creator
        self.responsible_supervisor = responsible_supervisor
        self.content = content

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "creator": self.creator,
            "responsible_supervisor": self.responsible_supervisor,
            "content": self.content,
        }


def insert_product(json_body: dict) -> InsertOneResult:
    c = collection.get_collection_instance(collection_products)

    product_document = {
        "uuid": uuid.uuid4().hex,
        "creator": json_body["creator"],
        "responsible_supervisor": json_body["responsible_supervisor"],
        "content": json_body["content"],
    }
    try:
        result = c.insert_one(product_document)
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def get_product_by_uuid(uuid: str):
    product_document = {
        "uuid": uuid,
    }
    c = collection.get_collection_instance(collection_products)
    try:
        result = c.find_one(product_document)
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def get_product_by_page(creator: str, responsible_supervisor: str, page: int, page_size: int):
    if creator is None:
        product_document = {
            "responsible_supervisor": responsible_supervisor,
        }
    if responsible_supervisor is None:
        product_document = {
            "creator": creator,
        }
    c = collection.get_collection_instance(collection_products)
    try:
        # Can be iterated by for loop
        result = c.find_by_page(product_document, page, page_size)
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def update_product(new_product: Product):
    product_document = {
        "uuid": new_product.uuid,
    }

    c = collection.get_collection_instance(collection_products)
    original_product = get_product_by_uuid(new_product.uuid)

    if new_product.responsible_supervisor is None:
        new_product.responsible_supervisor = original_product.get("responsible_supervisor")
    if new_product.content is None:
        new_product.content = original_product.get("content")
    try:
        result = c.update_one(product_document,
                              {"$set": {"responsible_supervisor": new_product.responsible_supervisor
                                  , "content": new_product.content}})
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def delete_product_by_uuid(uuid: str) -> DeleteResult:
    product_document = {
        "uuid": uuid,
    }
    c = collection.get_collection_instance(collection_products)
    try:
        result = c.delete_one(product_document)
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def delete_product_by_creator(creator: str) -> DeleteResult:
    product_document = {
        "creator": creator,
    }
    c = collection.get_collection_instance(collection_products)
    try:
        result = c.delete_many(product_document)
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error
