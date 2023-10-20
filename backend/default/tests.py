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


from default.db import connection

connection.create_collection("new_one")
conn = connection.get_collection_instance("test")
print(conn.list_collection())
conn.insert_one({
    "name": "test",
    "message": "123"
})
