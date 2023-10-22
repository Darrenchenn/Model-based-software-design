# Create your views here.
import json
import logging

logger = logging.getLogger('django')

from django.http import HttpResponse

from default.creator import chatgpt, stablediffusion
from default.common import error


# creator interfaces
def generate_noval_text(request):
    if request.method == "POST":
        error.Error("request method is wrong").http_response_new()
    prompt = request.GET.get("prompt")
    system = request.GET.get("system") if request.GET.get("system") is not None else ""
    gpt = chatgpt.ChatGpt(system)
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

    init_image = body["init_image"] if "init_image" in body else ""
    if init_image == "":
        return HttpResponse(sd.text_to_pic())
    else:
        return HttpResponse(sd.pic_to_pic(init_image))

# products interfaces

# message interfaces

# archive interfaces

# user interfaces


# template interfaces
