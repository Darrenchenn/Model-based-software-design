# products storage functions
import uuid
import pymongo

from pymongo.results import InsertOneResult, DeleteResult

from db import collectionnames, collection


class Product:

    def __init__(self, creator: str, responsible_supervisor: str = None) -> None:
        self.uuid = uuid.uuid4().hex
        self.creator = creator
        self.responsible_supervisor = responsible_supervisor


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
    
def get_product_by_uuid(uuid:str):
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
    
def get_product_by_creator_and_page(creator:str, page:int, page_size:int):
    product_document = {
        "creator": creator,
    }
    c = collection.get_collection_instance(collectionnames.collection_products)
    try:
        # Can be iterated by for loop
        result = c.find(product_document).skip((page - 1) * page_size).limit(page_size)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result
    
def get_product_by_supervisor_and_page(supervisor:str, page:int, page_size:int):
    product_document = {
        "responsible_supervisor": supervisor,
    }
    c = collection.get_collection_instance(collectionnames.collection_products)
    try:
        # Can be iterated by for loop
        result = c.find(product_document).skip((page - 1) * page_size).limit(page_size)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result
    
def update_product(product:Product):
    c = collection.get_collection_instance(collectionnames.collection_products)
    try:
        result = c.update_one({"uuid": product.uuid}, {"$set": {"responsible_supervisor": product.responsible_supervisor}})
    except pymongo.errors.OperationFailure:
        return None
    else:    
        return result

def get_product_by_uuid(uuid:str):
    product_document = {
        "uuid": uuid,
    }
    c = collection.get_collection_instance(collectionnames.collection_products)
    try:
        result = c.find_one(product_document)
    except:
        return None
    else:
        return result

def delete_product_by_uuid(uuid:str)->DeleteResult:
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
    
def delete_product_by_creator(creator:str)->DeleteResult:
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
