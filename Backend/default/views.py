# Create your views here.
import json
import logging

logger = logging.getLogger('django')

from django.http import HttpResponse

from default.creator import chatgpt, stablediffusion
from default.common import error

from Backend.default.metadata import product


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


# products interfaces


def get_product_by_uuid(request):
    if request.method != "GET":
        return HttpResponse(error.Error("request method is wrong").http_response_new())
    logger.info(request.GET)
    uuid = request.GET.get("uuid")
    if uuid is None:
        return HttpResponse(error.Error("uuid is None").http_response_new())
    result = product.get_product_by_uuid(uuid)
    if isinstance(result, error.Error):
        return HttpResponse(result.http_response_new())
    json_result = {
        "uuid": result["uuid"],
        "creator": result["creator"],
        "responsible_supervisor": result["responsible_supervisor"],
    }
    return HttpResponse(json.dumps(json_result))


def get_product_by_creator(request):
    if request.method != "GET":
        return HttpResponse(error.Error("request method is wrong").http_response_new())
    logger.info(request.GET)
    creator = request.GET.get("creator")
    page = request.GET.get("page")
    page_size = request.GET.get("page_size")
    if creator is None:
        return HttpResponse(error.Error("Parameters wrong").http_response_new())
    if page is None:
        page = 0
    if page_size is None:
        page_size = 10
    result = product.get_product_by_creator_and_page(creator, page, page_size)
    if isinstance(result, error.Error):
        return HttpResponse(result.http_response_new())
    json_result = []
    for i in result:
        json_result.append({
            "uuid": i["uuid"],
            "creator": i["creator"],
            "responsible_supervisor": i["responsible_supervisor"],
        })
    return HttpResponse(json.dumps(json_result))


def get_product_by_supervisor(request):
    if request.method != "GET":
        return HttpResponse(error.Error("request method is wrong").http_response_new())
    logger.info(request.GET)
    supervisor = request.GET.get("supervisor")
    page = request.GET.get("page")
    page_size = request.GET.get("page_size")
    if supervisor is None:
        return HttpResponse(error.Error("Parameters wrong").http_response_new())
    if page is None:
        page = 0
    if page_size is None:
        page_size = 10
    result = product.get_product_by_supervisor_and_page(supervisor, page, page_size)
    if isinstance(result, error.Error):
        return HttpResponse(result.http_response_new())
    json_result = []
    for i in result:
        json_result.append({
            "uuid": i["uuid"],
            "creator": i["creator"],
            "responsible_supervisor": i["responsible_supervisor"],
        })
    return HttpResponse(json.dumps(json_result))
# message interfaces

# archive interfaces

# user interfaces

# template interfaces
