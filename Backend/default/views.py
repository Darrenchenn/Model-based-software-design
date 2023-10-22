# Create your views here.
import json
import logging

logger = logging.getLogger('django')

from django.http import HttpResponse

from default.creator import chatgpt, stablediffusion
from default.common import error
from default.forwarding import wechat
from default.metadata import product


# creator interfaces
def generate_noval_text(request):
    if request.method == "POST":
        error.Error("request method is wrong").http_response_new()
    logger.info(request.GET)  # print request parameters which is easy for debugging.
    prompt = request.GET.get("prompt")
    system = request.GET.get("system") if request.GET.get("system") is not None else ""
    gpt = chatgpt.ChatGpt(system)
    return HttpResponse(gpt.talk(prompt))


def generate_image(request):
    if request.method == "GET":
        error.Error("request method is wrong").http_response_new()
    logger.info(request.POST)
    body = json.loads(request.body)
    api_key = body["api_key"] if "api_key" in body else ""
    prompt = body["prompt"] if "prompt" in body else ""
    width = body["width"] if "width" in body else ""
    height = body["height"] if "height" in body else ""
    # init parameters
    sd = stablediffusion.StableDiffusion(api_key, prompt, width, height)
    # if init_image is empty, creating image from only prompt.
    init_image = body["init_image"] if "init_image" in body else ""
    if init_image == "":
        return HttpResponse(sd.text_to_pic())
    else:
        return HttpResponse(sd.pic_to_pic(init_image))


# forwarding interfaces

def forward_wechat(request):
    if request.method == "POST":
        error.Error("request method is wrong").http_response_new()
    logger.info(request.GET)
    username = request.GET.get("username")
    title = request.GET.get("title")
    msg = request.GET.get("message")
    url = request.GET.get("url") if request.GET.get("url") is not None else ""
    wechat.forward(username, title, msg, url)
    return HttpResponse(wechat.forward(username, title, msg, url))


# products interfaces


def get_product(request):
    if request.method != "GET":
        return HttpResponse(error.Error("request method is wrong").http_response_new())
    logger.info(request.GET)
    uuid = request.GET.get("uuid")
    creator = request.GET.get("creator")
    responsible_supervisor = request.GET.get("responsible_supervisor")
    page = int(request.GET.get("page"))
    page_size = int(request.GET.get("page_size"))
    if uuid is not None and uuid is not '':
        result = product.get_product_by_uuid(uuid)
        if isinstance(result, error.Error):
            return HttpResponse(result.http_response_new())
        json_result = {
            "uuid": result["uuid"],
            "creator": result["creator"],
            "responsible_supervisor": result["responsible_supervisor"],
            "content": result["content"],
        }
        return HttpResponse(json.dumps(json_result))
    if page is None:
        page = 0
    if page_size is None:
        page_size = 10
    if creator is None or creator == '':
        creator = None
    if responsible_supervisor is None or responsible_supervisor == '':
        responsible_supervisor = None
    result = product.get_product_by_page(creator, responsible_supervisor, page, page_size)
    if isinstance(result, error.Error):
        return HttpResponse(result.http_response_new())
    json_result = []
    if result is None:
        return HttpResponse(json.dumps(json_result))
    for i in result:
        json_result.append({
            "uuid": i["uuid"],
            "creator": i["creator"],
            "responsible_supervisor": i["responsible_supervisor"],
            "content": i["content"],
        })
    return HttpResponse(json.dumps(json_result))


def insert_product(request):
    if request.method != "POST":
        return HttpResponse(error.Error("request method is wrong").http_response_new())
    logger.info(request.POST)
    body = json.loads(request.body)
    result = product.insert_product(body)
    if isinstance(result, error.Error):
        return HttpResponse(result.http_response_new())
    return HttpResponse()

# message interfaces

# archive interfaces

# user interfaces

# template interfaces
