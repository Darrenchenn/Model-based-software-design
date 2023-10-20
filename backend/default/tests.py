# Create your tests here.
from default.creator import chatgpt

system = input("system is :")
gpt = chatgpt.ChatGpt(system)

while True:
    prompt = input("prompt is :")
    if prompt == "q":
        break
    print(gpt.talk(prompt))
