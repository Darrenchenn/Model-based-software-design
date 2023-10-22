# # Create your tests here.
# from default.creator import chatgpt
#
# system = input("system is :")
# gpt = chatgpt.ChatGpt(system)
#
# while True:
#     prompt = input("prompt is :")
#     if prompt == "q":
#         break
#     print(gpt.talk(prompt))


# from default.db import collection
#
# # collection.create_collection("new_one")
# conn = collection.get_collection_instance("new_one")
# print(conn.list_collection())
# conn.insert_one({
#     "name": "test",
#     "message": "123"
# })


import datetime

from default.forwarding import wechat

current_time = datetime.datetime.now()
formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

msg = "This is a test msg sent at " + formatted_time

wechat.forward('Riianfar', msg, "wechat",
               'https://push.showdoc.com.cn/server/api/push/ead550a01d50a327901d77036528322a534410924')
