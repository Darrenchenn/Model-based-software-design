from django.shortcuts import render
from django.http import HttpResponse
from default.creator import creator
from default.news import news
from default.server import server
from default.user import users


# Create your views here.


def login(req):
    return users.usersResponse.login(req)
def generatePics(req):
    return creator.picsGenerationResponse.generatePics(req)

def generateText(req):
    return creator.picsGenerationResponse.generateText(req)

def newsList(req):
    return news.newsResponse.newsList(req)

def serverTest(req):
    return server.serverResponse.server(req)