# Do not use these functions directly,encrypted a new layer to call these functions in "metadata" directory.
from Backend.default.db import db_handle

db_instance, conn = db_handle.get_default_db_handle()


def get_collection_instance(connection_name):
    return Collection(db_instance, connection_name)


def create_collection(name):
    db_instance.create_collection(name)


def is_collection_exist(name):
    if name in get_collection_instance(name).list_collection():
        return True
    else:
        return False


class Collection:
    def __init__(self, db_instance, name):
        self.name = name
        self.db_instance = db_instance

    def get_collection(self):
        return self.db_instance[self.name]

    def list_collection(self):
        return self.db_instance.list_collection_names()

    def insert_one(self, data):
        return self.db_instance[self.name].insert_one(data)

    def insert_many(self, data):
        return self.db_instance[self.name].insert_many(data)

    def delete_one(self, data):
        return self.db_instance[self.name].delete_one(data)

    def delete_many(self, data):
        return self.db_instance[self.name].delete_many(data)

    def update_one(self, data, new_data):
        return self.db_instance[self.name].update_one(data, new_data)

    def update_many(self, data, new_data):
        return self.db_instance[self.name].update_many(data, new_data)

    def find_one(self, data):
        return self.db_instance[self.name].find_one(data)

    def find_one_and_delete(self, data):
        return self.db_instance[self.name].find_one_and_delete(data)

    def find_one_and_replace(self, data):
        return self.db_instance[self.name].find_one_and_replace(data)

    def find_one_and_update(self, data):
        return self.db_instance[self.name].find_one_and_update(data)

    def find(self, data):
        return self.db_instance[self.name].find(data)
    
    # Default page is 0, Default page size is 10
    def find_by_page(self, data, page:int=0, page_size:int=10):
        return self.db_instance[self.name].find(data).skip((page) * page_size).limit(page_size)
    
    def find_all_by_page(self, page:int=0, page_size:int=10):
        return self.db_instance[self.name].find().skip((page) * page_size).limit(page_size)

# medicine_1 = {
#    "medicine_id": "t01",
#    "common_name" : "testdata01",
#    "scientific_name" : "",
#    "available" : "Y",
#    "category": "fever"
# }
# medicine_2 = {
#    "medicine_id": "t02",
#    "common_name" : "testdata02",
#    "scientific_name" : "",
#    "available" : "Y",
#    "category" : "type 2 diabetes"
# }
# db,c = get_default_db_handle()
#
# a = connection(db,"test")
# print(a.list_collection())
#
# db_insert_many(get_db_connection_by_name(db,"test"),[medicine_1,medicine_2])
