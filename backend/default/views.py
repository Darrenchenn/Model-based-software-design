from django.shortcuts import render
from django.http import HttpResponse
from default.creator import creator
from default.news import news
from default.user import users


# Create your views here.
def generatePics(req):
    return creator.generatePics(req)
