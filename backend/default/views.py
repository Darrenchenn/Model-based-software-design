from django.shortcuts import render
from django.http import HttpResponse
from creator import generatePics,generateText

# Create your views here.



def GeneratePics(type,prompt):
    return generatePics(type,prompt)

def GenerateText(request):
    return generateText(request)