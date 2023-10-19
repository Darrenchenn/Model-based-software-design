# Write down all the function here.
import os
import openai

global_model = "gpt-3.5-turbo"
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
    current_model_list[msg](
        openai.ChatCompletion.create(
            model=get_model(),
            messages=[{"role": role, "content": msg}]
        )
    )


def get_api_model(msg):
    return current_model_list[msg]


def get_response(msg):
    return get_api_model(msg)['choices'][0]['message']['content']
