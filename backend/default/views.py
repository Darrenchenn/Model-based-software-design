# Create your views here.
import json

from django.http import HttpResponse

from default.creator import chatgpt, stablediffusioncreator

noval_system_prompt = "you are a noval writer."


def generate_noval_text(request):
    prompt = request.GET.get("prompt")
    gpt = chatgpt.ChatGpt(noval_system_prompt)
    return HttpResponse(gpt.talk(prompt))


def generate_image(request):
    body = json.loads(request.body)
    key = body["api_key"]
    prompt = body["prompt"]
    width = body["width"]
    height = body["height"]
    sd = stablediffusioncreator.StableDiffusion(key, prompt, width, height)
    return HttpResponse(sd.text_to_pic())
