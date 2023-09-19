from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi



def get_db_handle(db_name, host, port, username, password):
    if db_name == ""|host==""|port==""|username==""|password=="":
        return error("parameters can not be empty")

    client = MongoClient(host=host,
                         port=int(port),
                         username=username,
                         password=password
                         )
    db_handle = client['db_name']
    return db_handle, client

def get_db_handle_by_url(db_name,connection_string):
    if db_name == "" or connection_string=="":
        return error("db_name or connection_string can not be empty")

    client = MongoClient(connection_string)
    db_handle = client[db_name]
    return db_handle,client


class connection:
    def __init__(self,db_handle,name):
        self.name = name
        self.db_handle = db_handle

    def get_connection(self):
        return self.db_handle[self.name]

    def create_collection(self,collection_name):
        return self.db_handle[collection_name].create_collection()
    def list_collection(self):
        return self.db_handle.list_collection_names()

    def insert_one(self,data):
        return self.db_handle[self.name].insert_one(data)

    def insert_many(self,data):
        return self.db_handle[self.name].insert_many(data)

    def delete_one(self,data):
        return self.db_handle[self.name].delete_one(data)

    def delete_many(self,data):
        return self.db_handle[self.name].delete_many(data)

    def update_one(self,data):
        return self.db_handle[self.name].update_one(data)

    def update_many(self,data):
        return self.db_handle[self.name].update_many(data)

    def find_one(self,data):
        return self.db_handle[self.name].find_one(data)

    def find_one_and_delete(self,data):
        return self.db_handle[self.name].find_one_and_delete(data)

    def find_one_and_replace(self,data):
        return self.db_handle[self.name].find_one_and_replace(data)

    def find_one_and_update(self,data):
        return self.db_handle[self.name].find_one_and_update(data)

    def find(self,data):
        return self.db_handle[self.name].find(data)








#medicine_1 = {
#    "medicine_id": "t01",
#    "common_name" : "testdata01",
#    "scientific_name" : "",
#    "available" : "Y",
#    "category": "fever"
#}
#medicine_2 = {
#    "medicine_id": "t02",
#    "common_name" : "testdata02",
#    "scientific_name" : "",
#    "available" : "Y",
#    "category" : "type 2 diabetes"
#}
#db,c = get_db_handle_by_url("Cluster0","mongodb+srv://c1125105680:chen9611@cluster0.zluvrrd.mongodb.net/?retryWrites=true&w=majority")
#
#a = connection(db,"test")
#print(a.list_collection())

#db_insert_many(get_db_connection_by_name(db,"test"),[medicine_1,medicine_2])

