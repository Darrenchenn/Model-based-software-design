import configparser
import logging

from pymongo.mongo_client import MongoClient

from default.common import error

log = logging.getLogger('default')

config = configparser.ConfigParser()
config.read('config.ini')

url = config.get('mongodb', 'url')
cluster_name = config.get('mongodb', 'cluster_name')
log.info('url: %s--cluster_name: %s', url, cluster_name)
print('url: %s--cluster_name: %s' % (url, cluster_name))
# todo:these statements should be defined in config file.
db_default_url = url
db_default_name = cluster_name
print('url:', db_default_url)
print('cluster_name:', db_default_name)


# Mongo DB handle functions starts here.
def get_default_db_handle():
    if db_default_url == "" or db_default_name == "":
        return error.new("db_name or connection_string can not be empty")

    client = MongoClient(db_default_url)
    db_handle = client[db_default_name]
    return db_handle, client


def get_db_handle(db_name, host, port, username, password):
    if db_name == "" | host == "" | port == "" | username == "" | password == "":
        return error.new("parameters can not be empty")

    client = MongoClient(host=host,
                         port=int(port),
                         username=username,
                         password=password
                         )
    db_handle = client['db_name']
    return db_handle, client


def get_db_handle_by_url(db_name, connection_string):
    if db_name == "" or connection_string == "":
        return error.new("db_name or connection_string can not be empty")

    client = MongoClient(connection_string)
    db_handle = client[db_name]
    return db_handle, client
