import uuid
from pymongo.results import InsertOneResult, DeleteResult

from default.common.error import Error
from default.db import collection
from default.db.collectionnames import collection_products



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


def update_product(json_body: dict):
    product_document = {
        "uuid": json_body["uuid"],
    }
    c = collection.get_collection_instance(collection_products)
    try:
        original_product = c.find_one(product_document)
        if json_body["creator"] is None:
            json_body["creator"] = original_product.get("creator")
        if json_body["responsible_supervisor"] is None:
            json_body["responsible_supervisor"] = original_product.get("responsible_supervisor")
        if json_body["content"] is None:
            json_body["content"] = original_product.get("content")
        result = c.update_one(product_document, {"$set": json_body})
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