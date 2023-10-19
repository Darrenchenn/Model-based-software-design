from backend.default.creator.chatgpt import chatgpt

noval_system_prompt = "you are a noval writer."


def generate_noval_text(prompt):
    gpt = chatgpt.ChatGpt(noval_system_prompt)
    return gpt.talk(prompt)
