# Create your views here.
import json
import logging

logger = logging.getLogger('django')

from django.http import HttpResponse

from default.creator import chatgpt, stablediffusion
from default.common import error

noval_system_prompt = "you are a noval writer."


def generate_noval_text(request):
    if request.method == "POST":
        error.Error("request method is wrong").http_response_new()
    prompt = request.GET.get("prompt")
    gpt = chatgpt.ChatGpt(noval_system_prompt)
    return HttpResponse(gpt.talk(prompt))


def generate_image(request):
    if request.method == "GET":
        error.Error("request method is wrong").http_response_new()
    body = json.loads(request.body)
    api_key = body["api_key"] if "api_key" in body else ""
    prompt = body["prompt"] if "prompt" in body else ""
    width = body["width"] if "width" in body else ""
    height = body["height"] if "height" in body else ""

    sd = stablediffusion.StableDiffusion(api_key, prompt, width, height)
    return HttpResponse(sd.text_to_pic())
