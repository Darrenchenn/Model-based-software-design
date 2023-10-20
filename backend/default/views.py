# Create your views here.
from django.http import HttpResponse

from default.creator import chatgpt

noval_system_prompt = "you are a noval writer."


def generate_noval_text(request):
    prompt = request.GET.get("prompt")
    gpt = chatgpt.ChatGpt(noval_system_prompt)
    return HttpResponse(gpt.talk(prompt))
