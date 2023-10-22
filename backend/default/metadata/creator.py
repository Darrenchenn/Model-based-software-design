from backend.default.metadata.user import User
from default.db import collection

from default.db.collectionnames import collection_users


class Creator(User):
    def __init__(self, username, password=None, user_type=None, contact_info=None, liked_templates=None):
        super().__init__(username, password, user_type, contact_info)
        self.liked_template = liked_templates if liked_templates else []


def add_liked_template_by_user_uuid(user_uuid: str, template_uuid: str):
    c = collection.get_collection_instance(collection_users)
    result = c.find_one({"uuid": user_uuid})
    if result:
        liked_templates = result.get("liked_templates")
        if not liked_templates:
            liked_templates = []
        liked_templates.append(template_uuid)
        result = c.update_one({"uuid": user_uuid}, {"$set": {"liked_templates": liked_templates}})
    return result


def add_liked_template_by_username(username: str, template_uuid: str):
    c = collection.get_collection_instance(collection_users)
    result = c.find_one({"username": username})
    if result:
        liked_templates = result.get("liked_templates")
        if not liked_templates:
            liked_templates = []
        liked_templates.append(template_uuid)
        result = c.update_one({"username": username}, {"$set": {"liked_templates": liked_templates}})
    return result


def get_liked_template_by_username(username: str):
    c = collection.get_collection_instance(collection_users)
    result = c.find_one({"username": username})
    if result:
        liked_templates = result.get("liked_templates")
        if not liked_templates:
            liked_templates = []
        return liked_templates
    else:
        return []


def get_liked_template_by_user_uuid(uuid: str):
    c = collection.get_collection_instance(collection_users)
    result = c.find_one({"uuid": uuid})
    if result:
        liked_templates = result.get("liked_templates")
        if not liked_templates:
            liked_templates = []
        return liked_templates
    else:
        return []


def delete_liked_template(user: User, template_uuid: str):
    c = collection.get_collection_instance(collection_users)
    result = c.find_one({"username": user.username})
    if result:
        liked_templates = result.get("liked_templates")
        if not liked_templates:
            liked_templates = []
            return None
        liked_templates.remove(template_uuid)
        result = c.update_one({"username": user.username}, {"$set": {"liked_templates": liked_templates}})
    return result


def get_product_save(self, product_name):
    # TODO: 根据产品名称返回ProductSave对象
    pass
