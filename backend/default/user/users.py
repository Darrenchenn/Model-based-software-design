from django.shortcuts import render
from django.http import HttpResponse
import manage




class user:
    def __init__(self,name,password):
        self.name = name
        self.password = password

    def login(req):
        if req.method == "GET":
            return render(req,"login.html")

        print(req.POST)
        userName = req.POST.get("user")
        userPassword = req.POST.get("password")
        return HttpResponse("login success")
