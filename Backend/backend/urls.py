"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from default import views

urlpatterns = [
    # creator interfaces urls
    path('creator/', views.generate_noval_text),
    path('sd_creator/', views.generate_image),

    # forwarding interfaces urls
    path('forward/wechat', views.forward_wechat),

    # products interfaces urls
    path('get_product/', views.get_product),
    path('insert_product/', views.insert_product),

    # user interfaces urls
]
