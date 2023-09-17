from django.shortcuts import render
from django.http import HttpResponse
from default import creator


# Create your views here.



def GeneratePics(req):
    return creator.picsGenerationResponse.generatePics(req)

def GenerateText(req):
    return creator.picsGenerationResponse.generateText(req)