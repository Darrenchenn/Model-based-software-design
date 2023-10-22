import uuid

import pymongo
from pymongo.results import InsertOneResult

from Backend.default.db import collection
from Backend.default.db.collectionnames import collection_audits


class Audit:

    def __init__(self, result: bool = False, comment: list = [], creator: str = None,
                 responsible_supervisor: str = None) -> None:
        self.uuid = uuid.uuid4().hex
        self.result = result
        self.comment = comment
        self.creator = creator
        self.responsible_supervisor = responsible_supervisor

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "result": self.result,
            "comment": self.comment,
            "creator": self.creator,
            "responsible_supervisor": self.responsible_supervisor,
        }


def insert_audit(audit: Audit) -> InsertOneResult:
    c = collection.get_collection_instance(collection_audits)

    audit_document = {
        "uuid": audit.uuid,
        "result": audit.result,
        "comment": audit.comment,
        "creator": audit.creator,
        "responsible_supervisor": audit.responsible_supervisor,
    }

    try:
        result = c.insert_one(audit_document)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result


def get_audit_by_uuid(uuid: str):
    audit_document = {
        "uuid": uuid,
    }
    c = collection.get_collection_instance(collection_audits)
    try:
        result = c.find_one(audit_document)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result


def get_audit_by_creator_and_page(creator: str, page: int, page_size: int):
    audit_document = {
        "creator": creator,
    }
    c = collection.get_collection_instance(collection_audits)
    try:
        # Can be iterated by for loop
        result = c.find_all_by_page(audit_document, page, page_size)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result


def get_audit_by_supervisor_and_page(supervisor: str, page: int, page_size: int):
    audit_document = {
        "responsible_supervisor": supervisor,
    }
    c = collection.get_collection_instance(collection_audits)
    try:
        # Can be iterated by for loop
        result = c.find_all_by_page(audit_document, page, page_size)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result


def update_audit(new_audit: Audit):
    audit_document = {
        "uuid": new_audit.uuid,
    }
    c = collection.get_collection_instance(collection_audits)
    original_audit = c.find_one(audit_document)
    if new_audit.result is False:
        new_audit.result = original_audit.get("result")
    if new_audit.comment is []:
        new_audit.comment = original_audit.get("comment")
    if new_audit.creator is None:
        new_audit.creator = original_audit.get("creator")
    if new_audit.responsible_supervisor is None:
        new_audit.responsible_supervisor = original_audit.get("responsible_supervisor")
    new_values = {
        "$set": {
            "result": new_audit.result,
            "comment": new_audit.comment,
            "creator": new_audit.creator,
            "responsible_supervisor": new_audit.responsible_supervisor,
        }
    }
    try:
        result = c.update_one(audit_document, new_values)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result


def delete_audit_by_uuid(uuid: str):
    audit_document = {
        "uuid": uuid,
    }
    c = collection.get_collection_instance(collection_audits)
    try:
        result = c.delete_one(audit_document)
    except pymongo.errors.OperationFailure:
        return None
    else:
        return result
