#Write down all the function here.
from default import common
from django.http import HttpResponse
from django.shortcuts import render

def newsList(self):
    import requests
    res = requests.get("http://www.chinaunicom.com.cn/api/article/NewsByIndex/2/2023/09/news")
    data_list = res.text
    print(data_list)

    return render(self,"news.html", {"news_list":data_list})
