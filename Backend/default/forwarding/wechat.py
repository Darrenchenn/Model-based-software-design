import json
import logging

from default.common import http, error
from default.db import collection, collectionnames

log = logging.getLogger('default')


# This is used to forward messages to the WeChat public channel which needs user subscribe it first.
# If user already have a subscription url then it will use that url to forward the message.
# Otherwise,the url of this user is needed.
def forward(username, title, msg, url):
    try:
        conn = collection.get_collection_instance(collectionnames.collection_forwarding_urls)
        ret = conn.find_one({"name": username})
        if ret is None:
            if url is not None:
                conn.insert_one({"name": username, "url": url})
            else:
                return error.Error('url is None').new()
        else:
            if ret['url'] is not None:
                return error.new('The user has not registered.')
            return http.request(ret['url'], 'GET', json.dumps({
                "title": title,
                "content": msg,
            }))
    except error.Error as e:
        error.new("Failed to forward,err: %s" % e.message)
