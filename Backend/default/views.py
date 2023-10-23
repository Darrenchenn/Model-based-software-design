# Create your views here.
import json
import logging

logger = logging.getLogger('django')

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse

from default.creator import chatgpt, stablediffusion
from default.common import error
from default.forwarding import wechat
from default.products import product_service


# creator interfaces
def generate_noval_text(request):
    if request.method == "POST":
        return HttpResponseBadRequest(JsonResponse({
            "error": error.new("request method is wrong"),
        }))
    logger.info(request.GET)  # print request parameters which is easy for debugging.
    prompt = request.GET.get("prompt")
    system = request.GET.get("system") if request.GET.get("system") is not None else ""
    gpt = chatgpt.ChatGpt(system)
    return HttpResponse(gpt.talk(prompt))


def generate_image(request):
    if request.method == "GET":
        return HttpResponseBadRequest(JsonResponse({
            "error": error.new("request method is wrong"),
        }))
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
        return HttpResponseBadRequest(JsonResponse({
            "error": error.new("request method is wrong"),
        }))
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
        return HttpResponseBadRequest(JsonResponse({
            "error": error.new("request method is wrong"),
        }))
    logger.info(request.GET)

    uuid = request.GET.get("uuid") or None
    page = int(request.GET.get("page")) if request.GET.get("page") else 0
    page_size = int(request.GET.get("page_size")) if request.GET.get("page_size") else 10
    creator_uuid = request.GET.get("creator_uuid") or None
    creator_name = request.GET.get("creator_name") or None
    responsible_supervisor_uuid = request.GET.get("responsible_supervisor_uuid") or None
    responsible_supervisor_name = request.GET.get("responsible_supervisor_name") or None

    if uuid:
        json_result = product_service.get_product_by_uuid(uuid)
        if isinstance(json_result, error.Error):
            return HttpResponseBadRequest(JsonResponse({
                "error": error.new(),
            }))
        return HttpResponse(json_result)

    json_result = product_service.get_product_by_page(creator_uuid,
                                                    creator_name,
                                                    responsible_supervisor_uuid,
                                                    responsible_supervisor_name,
                                                    page,
                                                    page_size)
    if isinstance(json_result, error.Error):
        return HttpResponseBadRequest(JsonResponse({
            "error": error.new(),
        }))
    return HttpResponse(json_result)


def get_product_by_audition_status(request):
    if request.method != "GET":
        return HttpResponseBadRequest(JsonResponse({
            "error": error.new("request method is wrong"),
        }))
    logger.info(request.GET)

    audition_status = request.GET.get("audition_status") or None
    page = int(request.GET.get("page")) if request.GET.get("page") else 0
    page_size = int(request.GET.get("page_size")) if request.GET.get("page_size") else 10

    json_result = product_service.get_product_by_audition_status(audition_status, page, page_size)
    if isinstance(json_result, error.Error):
        return HttpResponseBadRequest(JsonResponse({
            "error": error.new(),
        }))
    return HttpResponse(json_result)


def insert_product(request):
    if request.method != "POST":
        return HttpResponseBadRequest(JsonResponse({
            "error": error.new("request method is wrong"),
        }))
    logger.info(request.POST)
    body = json.loads(request.body)
    json_result = product_service.insert_product(body)
    if isinstance(json_result, error.Error):
        return HttpResponseBadRequest(JsonResponse({
            "error": error.new(),
        }))
    return HttpResponse(json_result)


def update_product(request):
    if request.method != "POST":
        return HttpResponseBadRequest(JsonResponse({
            "error": error.new("request method is wrong"),
        }))
    logger.info(request.POST)
    body = json.loads(request.body)
    result = product_service.update_product(body)
    if isinstance(result, error.Error):
        return HttpResponseBadRequest(JsonResponse({
            "error": error.new(),
        }))
    return HttpResponse()

# message interfaces

# archive interfaces

# user interfaces

# template interfaces
