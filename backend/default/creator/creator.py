#Write down all the function here.
from default import common
from django.http import HttpResponse
from django.shortcuts import render



class picsGenerationResponse:
    def __init__(self):
        self.type = type

    def generatePics(req):
        return render(req,"test.html")





class textGenerationResponse:
    def __init__(self):
        self.type = type

    def generateText(req):
        return HttpResponse("welcome.")