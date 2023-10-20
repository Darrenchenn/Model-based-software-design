from backend.default.metadata.user import User

from default.db import connection

user_collection_name = "users"

class Creator(User):
    def __init__(self, username, password=None, user_type=None, contact_info=None, liked_templates=None):
        super().__init__(username, password, user_type, contact_info)
        self.liked_template = liked_templates if liked_templates else []


def add_liked_template(user:User, template_id:str):
    c = connection.get_collection(user_collection_name)
    result = c.find_one({"username": user.username})

    if result:
        liked_templates = result.get("liked_templates")
        if not liked_templates:
            liked_templates = []
        liked_templates.append(template_id)
        result = c.update_one({"username": user.username}, {"$set": {"liked_templates": liked_templates}})

    return result


def get_liked_template(user:User):
    c = connection.get_collection(user_collection_name)
    result = c.find_one({"username": user.username})
    if result:
        liked_templates = result.get("liked_templates")
        if not liked_templates:
            liked_templates = []
        return liked_templates
    else:
        return []


    def get_product_save(self, product_name):
        # TODO: 根据产品名称返回ProductSave对象
        pass
