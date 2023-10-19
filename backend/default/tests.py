# Create your tests here.
from creator.chatgpt import chatgpt

chatgpt.create_api_model("user", "帮我翻译成法语")
print(chatgpt.get_response("帮我翻译成法语"))
