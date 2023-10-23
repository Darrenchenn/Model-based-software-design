import json
import uuid
from pymongo.results import InsertOneResult, DeleteResult

from default.common.error import Error
from default.db import collection
from default.db.collectionnames import collection_products



def insert_product(json_body: dict) -> InsertOneResult:
    c = collection.get_collection_instance(collection_products)

    product_document = {
        "uuid": uuid.uuid4().hex,
        "creator_uuid": json_body["creator_uuid"],
        "creator_name": json_body["creator_name"],
        "responsible_supervisor_uuid": json_body["responsible_supervisor_uuid"],
        "responsible_supervisor_name": json_body["responsible_supervisor_name"],
        "audition_status": json_body["audition_status"],
        "audit_comment": json_body["audit_comment"],
        "content": json_body["content"],
    }
    try:
        c.insert_one(product_document)
        return json.dumps(product_document["uuid"])
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
        json_result = {
            "uuid": result["uuid"],
            "creator_uuid": result["creator_uuid"],
            "creator_name": result["creator_name"],
            "responsible_supervisor_uuid": result["responsible_supervisor_uuid"],
            "responsible_supervisor_name": result["responsible_supervisor_name"],
            "audition_status": result["audition_status"],
            "audit_comment": result["audit_comment"],
            "content": result["content"],
        }
        return json.dumps(json_result)
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error


def get_product_by_page(creator_uuid: str,
                        creator_name: str,
                        responsible_supervisor_uuid: str,
                        responsible_supervisor_name: str,
                        page: int,
                        page_size: int):
    product_document = {}
    if creator_uuid:
        product_document["creator_uuid"] = creator_uuid
    if creator_name:
        product_document["creator_name"] = creator_name
    if responsible_supervisor_uuid:
        product_document["responsible_supervisor_uuid"] = responsible_supervisor_uuid
    if responsible_supervisor_name:
        product_document["responsible_supervisor_name"] = responsible_supervisor_name
    c = collection.get_collection_instance(collection_products)
    try:
        # Can be iterated by for loop
        result = c.find_by_page(product_document, page, page_size)
        json_result = []
        for i in result:
            json_result.append({
                "uuid": i["uuid"],
                "creator_uuid": i["creator_uuid"],
                "creator_name": i["creator_name"],
                "responsible_supervisor_uuid": i["responsible_supervisor_uuid"],
                "responsible_supervisor_name": i["responsible_supervisor_name"],
                "audition_status": i["audition_status"],
                "audit_comment": i["audit_comment"],
                "content": i["content"],
            })
        return json.dumps(json_result)
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error
    

def get_product_by_audition_status(audition_status: str, page: int, page_size: int):
    
    product_document = {
        "audition_status": audition_status if audition_status else "unaudited",
    }
    c = collection.get_collection_instance(collection_products)
    try:
        result = c.find_by_page(product_document, page, page_size)
        json_result = []
        for i in result:
            json_result.append({
                "uuid": i["uuid"],
                "creator_uuid": i["creator_uuid"],
                "creator_name": i["creator_name"],
                "responsible_supervisor_uuid": i["responsible_supervisor_uuid"],
                "responsible_supervisor_name": i["responsible_supervisor_name"],
                "audition_status": i["audition_status"],
                "audit_comment": i["audit_comment"],
                "content": i["content"],
            })
        return json.dumps(json_result)
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
        if original_product is None:
            error = Error("Product not found")
            error.new()
            return error
        creator_uuid = json_body["creator_uuid"] if json_body.get("creator_uuid") else original_product["creator_uuid"]
        creator_name = json_body["creator_name"] if json_body.get("creator_name") else original_product["creator_name"]
        responsible_supervisor_uuid = json_body["responsible_supervisor_uuid"] if json_body.get("responsible_supervisor_uuid") else original_product["responsible_supervisor_uuid"]
        responsible_supervisor_name = json_body["responsible_supervisor_name"] if json_body.get("responsible_supervisor_name") else original_product["responsible_supervisor_name"]
        audition_status = json_body["audition_status"] if json_body.get("audition_status") else original_product["audition_status"]
        audit_comment = json_body["audit_comment"] if json_body.get("audit_comment") else original_product["audit_comment"]
        content = json_body["content"] if json_body.get("content") else original_product["content"]
        new_product = {
            "$set": {
                "creator_uuid": creator_uuid,
                "creator_name": creator_name,
                "responsible_supervisor_uuid": responsible_supervisor_uuid,
                "responsible_supervisor_name": responsible_supervisor_name,
                "audition_status": audition_status,
                "audit_comment": audit_comment,
                "content": content,
            }
        }
        result = c.update_one(product_document, new_product)
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


def delete_product_by_creator(creator_uuid:str=None, creator_name:str=None) -> DeleteResult:
    c = collection.get_collection_instance(collection_products)
    if creator_uuid:
        product_document = {
            "creator_uuid": creator_uuid,
        }
    elif creator_name:
        product_document = {
            "creator_name": creator_name,
        }
    try:
        result = c.delete_many(product_document)
        return result
    except Exception as e:
        error = Error(f"An unexpected error occurred: {str(e)}")
        error.new()
        return error