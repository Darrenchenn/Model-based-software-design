# Write down all the function here.
import openai

global_model = "gpt-3.5-turbo-0613"
current_model_list = {}


def get_api_key():
    # todo: set this key in configure file.
    return "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"


def get_api_organization():
    return "org-gMxHGfwHj3upRlzVepNzbAJy"


def set_model(new_model):
    global_model = new_model


def get_model():
    return global_model


def create_api_model(role, msg):
    openai.api_key = get_api_key()
    current_model_list[msg] = openai.ChatCompletion.create(
        model=get_model(),
        messages=[{"role": role, "content": msg}]
    )

    # todo: add created ChatCompletion to database.


def delete_api_model(msg):
    # todo:delete ChatCompletion from database.
    del current_model_list[msg]


def get_api_model(msg):
    return current_model_list[msg]


def get_response(msg):
    return get_api_model(msg)['choices'][0]['message']['content']
