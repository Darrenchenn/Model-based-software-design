from django.shortcuts import render
from django.http import HttpResponse

class usersResponse:
    def login(req):
        if req.method == "GET":
            return render(req,"login.html")
        else:
            print(req.POST)
            userName = req.POST.get("user")
            userPassword = req.POST.get("password")
            return HttpResponse("login success")