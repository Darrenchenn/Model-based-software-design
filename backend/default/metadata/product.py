# products storage functions
import uuid

import pymongo
from pymongo.results import InsertOneResult

from default.db import connection

product_collection_name = "products"


class Product:

    def __init__(self, creator: str, responsible_supervisor: str = None) -> None:
        self.uuid = uuid.uuid4().hex
        self.creator = creator
        self.responsible_supervisor = responsible_supervisor


def insert_product(product: Product) -> InsertOneResult:
    c = connection.get_db_instance(product_collection_name)

    product_document = {
        "uuid": product.uuid,
        "responsible_supervisor": product.responsible_supervisor,
    }

    try:
        result = c.insert_one(product_document)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result


insert_product()
