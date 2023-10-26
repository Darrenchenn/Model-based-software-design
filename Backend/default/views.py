# Create your views here.
import json
import logging

from default.metadata.template import get_content_by_uuid

logger = logging.getLogger('django')

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse

from default.creator import chatgpt, stablediffusion
from default.common import error
from default.forwarding import wechat
from default.forwarding import email_forwarding
from default.products import product_service
from default.metadata.template import Template, insert_template, get_template, update_template, \
    delete_template_by_uuid, get_all_template_by_page
from default.metadata.user import User,insert_user, get_user_by_username, update_user, get_user_by_uuid, ContactInfo,get_all_users_by_page
from default.common.error import Error


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

def forward_email(request):
    if request.method != "GET":
        return HttpResponseBadRequest(JsonResponse({
            "error": error.new("request method is wrong"),
        }))
    logger.info(request.GET)
    recipient_email = request.GET.get("recipient_email")
    subject = request.GET.get("subject")
    message = request.GET.get("message")
    return HttpResponse(email_forwarding.forward_email(recipient_email, subject, message))


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
# User register interfaces
def register_user(request):
    if request.method == "POST":
        try:
            # 访问表单字段而不是尝试解析 JSON 数据
            username = request.POST.get("username")
            password = request.POST.get("password")
            user_type = request.POST.get("user_type")
            email = request.POST.get("email")
            wechat_id = request.POST.get("wechat_id")

            if username and password:
                contact_info = ContactInfo(email = email,wechat_id = wechat_id)
                # 创建注册
                user = User(username, password, user_type,contact_info.to_dict())

                # 插入用户
                result = insert_user(user)
                if isinstance(result,Error):
                    return JsonResponse({"error": result.message})
                else:
                    user = get_user_by_username(username)
                    return JsonResponse({"uuid": user["uuid"],"username":user["username"],"user_type":user["user_type"],"contact_info":user["contact_info"]})
            else:
                return JsonResponse({"error": "Username and Password are required"})
        except Exception as e:
            return JsonResponse({"error": "An error occurred: " + str(e)})
    else:
        return JsonResponse({"error": "Invalid request method"})



# User Login interfaces
def login_user(request):
    if request.method == "POST":
        try:
            # analyse request data
            #data = json.loads(request.body)
            username = request.POST.get("username")
            password = request.POST.get("password")

            # capture user information
            if username and password:
                user = get_user_by_username(username)
                # user do not exist
                if not user:
                    return JsonResponse({"error": "User not found"})
                # validate password
                if user["password"] == password:
                    return JsonResponse({"uuid": user["uuid"],"username":user["username"],"user_type":user["user_type"],"contact_info":user["contact_info"]})
                else:
                    return JsonResponse({"error": "Invalid password"})
            else:
                return JsonResponse({"error": "Username and Password are required"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"})
    else:
        return JsonResponse({"error": "Invalid request method"})


# User update interfaces
def update_user_info(request, uuid):
    if request.method == "POST":
        try:
            # 解析请求中的POST数据

            # 获取要更新的用户信息，基于UUID
            user_data = get_user_by_uuid(uuid)

            if not isinstance(user_data, dict):
                return JsonResponse({"error": "User not found"})

            # 创建 User 对象
            user = User(
                username=user_data.get("username"),
                password=user_data.get("password"),
                user_type=user_data.get("user_type"),
                contact_info=user_data.get("contact_info"),

            )

            # 更新用户信息
            if "password" in request.POST:
                user.password = request.POST["password"]
            if "user_type" in request.POST:
                user.user_type = request.POST["user_type"]
            if "email" in request.POST:
                email = request.POST["email"]
            if "wechat_id" in request.POST:
                wechat_id = request.POST["wechat_id"]
            contact_info_new = ContactInfo(email=email, wechat_id=wechat_id)
            user.contact_info = contact_info_new.to_dict()
            # 执行更新操作
            result = update_user(user)  # 实现此方法来更新用户信息

            if result:
                user = get_user_by_uuid(uuid)
                return JsonResponse({"uuid": user["uuid"], "username": user["username"], "user_type": user["user_type"],
                                     "contact_info": user["contact_info"]})
            else:
                return JsonResponse({"error": "Failed to update user data"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"})
    else:
        return JsonResponse({"error": "Invalid request method"})


def verify_supervisor(request,uuid):
    if request.method == "GET":
        try:
            user = get_user_by_uuid(uuid)
            if user:
                user_type = user['user_type']
                if user_type == "supervisor":
                    return JsonResponse({"message":"success","supervisor_id": user["uuid"], "supervisor_namae": user["username"], "user_type": user["user_type"],
                                         "contact_info": user["contact_info"]})
                else:
                    return JsonResponse({"error":"not a valid supervisor id"})
            else:
                return JsonResponse({"error":"not a valid supervisor id"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid request method"})
    else:
        return JsonResponse({"error": "Invalid request method"})

# get all users
def get_all_users(request):
    if request.method == "GET":
        try:
            page = request.GET.get("page", 1)
            page_size = request.GET.get("page_size", 10)

            page = int(page) if page.isdigit() else 1
            page_size = int(page_size) if page_size.isdigit() else 10

            cursor = get_all_users_by_page(page, page_size)

            if isinstance(cursor, Error):
                return JsonResponse({"error": str(cursor)}, status=400)

            # 将Cursor对象中的数据转换为列表，同时将ObjectId对象转换为字符串
            users = []
            for document in cursor:
                user = {
                    "uuid": str(document.get("uuid")),  # 将ObjectId转换为字符串
                    "username": str(document.get("username")),
                    "user_type":str(document.get("user_type")),
                    "contact_info":str(document.get("user_type")),
                    # "email":document.get("contact_info",[]),
                    # "wechat_id":document.get("contact_info",[])
                }
                users.append(user)

            return JsonResponse(users, safe=False)
        except Exception as e:
            error_message = str(e)
            return JsonResponse({"error": error_message}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

# get user info
def get_user_info(request, uuid):
    if request.method == "GET":
        # Get user information based on username
        user = get_user_by_uuid(uuid)
        if user:
            # Create a JSON response that contains user information
            user_info = {
                "username": user["username"],
                "user_type": user["user_type"],
                "contact_info": user["contact_info"]
            }
            return JsonResponse(user_info)
        else:
            return JsonResponse({"error": "User not found"})
    else:
        return JsonResponse({"error": "Invalid request method"})


# template interfaces
# create template interface
def create_template(request):
    if request.method == "POST":
        # get template data from the request
        data = request.POST
        content = data.get("content", [])

        # create template object
        template = Template(content=content)

        # insert template to database
        result = insert_template(template)

        if result:
            return JsonResponse({"message": "Template created successfully"})
        else:
            return JsonResponse({"error": "Failed to create template"})
    else:
        return JsonResponse({"error": "Invalid request method"})


# obtain template interface
def get_template_content_by_uuid(request, uuid):
    if request.method == "GET":
        template_content = get_content_by_uuid(uuid)

        if template_content:
            return JsonResponse(template_content, safe=False)
        else:
            return JsonResponse({"error": "Template not found"})
    else:
        return JsonResponse({"error": "Invalid request method"})



# update template interface
def update_template_by_uuid(request, uuid):
    if request.method == "POST":
        # 获取请求中的内容
        content = request.POST.get("content", [])

        # 创建一个新的 Template 对象
        existing_template = Template(content=content)

        # 手动设置 uuid 属性
        existing_template.uuid = uuid

        # 更新模板
        result = update_template(existing_template)

        if result:
            return JsonResponse({"message": "Template updated successfully"})
        else:
            return JsonResponse({"error": "Failed to update template"})
    else:
        return JsonResponse({"error": "Invalid request method"})


# delete template interface
def delete_template(request, uuid):
    if request.method == "GET":
        result = delete_template_by_uuid(uuid)  # 调用你之前定义的函数

        if result.deleted_count > 0:
            return JsonResponse({"message": "Template deleted successfully"})
        else:
            return JsonResponse({"error": "Template not found for UUID: " + uuid}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)





# obtain all templates interface

def get_all_templates(request):
    if request.method == "GET":
        try:
            page = request.GET.get("page", 1)
            page_size = request.GET.get("page_size", 10)

            page = int(page) if page.isdigit() else 1
            page_size = int(page_size) if page_size.isdigit() else 10

            cursor = get_all_template_by_page(page, page_size)

            if isinstance(cursor, Error):
                return JsonResponse({"error": str(cursor)}, status=400)

            # 将Cursor对象中的数据转换为列表，同时将ObjectId对象转换为字符串
            templates = []
            for document in cursor:
                template = {
                    "uuid": str(document.get("uuid")),  # 将ObjectId转换为字符串
                    "content": document.get("content", [])
                }
                templates.append(template)

            return JsonResponse(templates, safe=False)
        except Exception as e:
            error_message = str(e)
            return JsonResponse({"error": error_message}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

