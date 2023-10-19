# Write down all the function here.
import openai

global_model = "gpt-3.5-turbo-0613"


def get_api_key():
    # todo: set this key in configure file.
    return "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"


def get_api_organization():
    return "org-gMxHGfwHj3upRlzVepNzbAJy"


def set_model(new_model):
    global_model = new_model


def get_model():
    return global_model


class ChatGpt:
    def __init__(self, system):
        self.api_key = get_api_key()
        self.message = []
        self.system = system
        self.assistant = ""
        openai.api_key = get_api_key()

        if self.system != "":
            self.message.append({"role": "system", "content": self.system})

    def query(self, msg):
        self.message.append({"role": "user", "content": msg})
        model = openai.ChatCompletion.create(
            model=get_model(),
            messages=self.message
        )
        self.assistant = model['choices'][0]['message']['content']
        return self.assistant

        # todo: add created ChatCompletion to database.

    def talk(self, msg):
        if self.assistant != "":
            self.message.append({"role": "assistant", "content": self.assistant})
        if msg != "":
            self.message.append({"role": "user", "content": msg})
        model = openai.ChatCompletion.create(
            model=get_model(),
            messages=self.message
        )

        self.assistant = model['choices'][0]['message']['content']
        return self.assistant

        # todo: add created ChatCompletion to database.
