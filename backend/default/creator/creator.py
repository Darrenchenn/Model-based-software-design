#Write down all the function here.
from default import common
from django.http import HttpResponse
from django.shortcuts import render




def generatePics(req):
    return render(req,"test.html")



