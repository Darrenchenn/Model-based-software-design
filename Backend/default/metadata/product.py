# products storage functions
import uuid

import pymongo
from pymongo.results import InsertOneResult, DeleteResult

from default.db import collectionnames, collection


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


def insert_product(product: Product) -> InsertOneResult:
    c = collection.get_collection_instance(collectionnames.collection_products)

    product_document = {
        "uuid": product.uuid,
        "creator": product.creator,
        "responsible_supervisor": product.responsible_supervisor,
    }
    try:
        result = c.insert_one(product_document)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result


def get_product_by_uuid(uuid: str):
    product_document = {
        "uuid": uuid,
    }
    c = collection.get_collection_instance(collectionnames.collection_products)
    try:
        result = c.find_one(product_document)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result


def get_product_by_creator_and_page(creator: str, page: int, page_size: int):
    product_document = {
        "creator": creator,
    }
    c = collection.get_collection_instance(collectionnames.collection_products)
    try:
        # Can be iterated by for loop
        result = c.find_all_by_page(product_document, page, page_size)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result


def get_product_by_supervisor_and_page(supervisor: str, page: int, page_size: int):
    product_document = {
        "responsible_supervisor": supervisor,
    }
    c = collection.get_collection_instance(collectionnames.collection_products)
    try:
        # Can be iterated by for loop
        result = c.find_all_by_page(product_document, page, page_size)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result


def update_product(new_product: Product):
    product_document = {
        "uuid": new_product.uuid,
    }

    c = collection.get_collection_instance(collectionnames.collection_products)
    original_product = get_product_by_uuid(new_product.uuid)

    if new_product.responsible_supervisor is None:
        new_product.responsible_supervisor = original_product.get("responsible_supervisor")
    if new_product.content is None:
        new_product.content = original_product.get("content")
    try:
        result = c.update_one(product_document,
                              {"$set": {"responsible_supervisor": new_product.responsible_supervisor
                                  , "content": new_product.content}})
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result


def delete_product_by_uuid(uuid: str) -> DeleteResult:
    product_document = {
        "uuid": uuid,
    }
    c = collection.get_collection_instance(collectionnames.collection_products)
    try:
        result = c.delete_one(product_document)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result


def delete_product_by_creator(creator: str) -> DeleteResult:
    product_document = {
        "creator": creator,
    }
    c = collection.get_collection_instance(collectionnames.collection_products)
    try:
        result = c.delete_many(product_document)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result
