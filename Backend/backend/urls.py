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
    path('get_product_by_audition_status/', views.get_product_by_audition_status),
    path('insert_product/', views.insert_product),
    path('update_product/', views.update_product),

    # user interfaces urls
    path('register_user/',views.register_user),
    path('login_user/',views.login_user),
    path('update_user_info/<str:uuid>/',views.update_user_info),
    path('get_user_info/<str:uuid>/', views.get_user_info,name='get_user_info'),
    path('verify_supervisor/<str:uuid>/', views.verify_supervisor, name='verify_superviorr'),
    path('get_all_users/',views.get_all_users),

    # template interfaces urls
    path('create_template/',views.create_template),
    path('get_template_content_by_uuid/<str:uuid>/', views.get_template_content_by_uuid, name='get_template_content_by_uuid'),
    path('update_template_by_uuid/<str:uuid>/', views.update_template_by_uuid),
    path('delete_template/<str:uuid>/', views.delete_template, name='delete_template'),
    path('get_all_templates/',views.get_all_templates),



]
