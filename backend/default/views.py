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
    if request.method == "POST":
        json_data = json.loads(request.body)
        key = json_data["key"]
        prompt = json_data["prompt"]
        width = json_data["width"]
        height = json_data["height"]

    sd = stablediffusioncreator.StableDiffusion(key, prompt, width, height)
    return HttpResponse(sd.text_to_pic())
