# products storage functions
import uuid

from pymongo.results import InsertOneResult

from default.db import collectionnames, collection


class Product:

    def __init__(self, creator: str, responsible_supervisor: str = None) -> None:
        self.uuid = uuid.uuid4().hex
        self.creator = creator
        self.responsible_supervisor = responsible_supervisor


def insert_product(product: Product) -> InsertOneResult:
    if collection.is_collection_exist(collectionnames.collection_products):
        # todo: do insertion
    else:
        collection.create_collection(collectionnames.collection_products)
        # todo: do insertion

