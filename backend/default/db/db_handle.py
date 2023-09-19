from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

db_url_default = "mongodb+srv://c1125105680:chen9611@cluster0.zluvrrd.mongodb.net/?retryWrites=true&w=majority"
db_name_default = "Cluster0"


def get_default_db_handle():
    if db_url_default == "" or db_name_default=="":
        return error("db_name or connection_string can not be empty")

    client = MongoClient(db_url_default)
    db_handle = client[db_name_default]
    return db_handle,client


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
