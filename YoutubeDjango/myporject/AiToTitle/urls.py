from django.urls import path,re_path
from . import views
from django.conf.urls import url  #導入url套件
app_name='AiToTitle'

from django.conf.urls import url, include
from django.contrib import admin
# app_name = 'blog'


urlpatterns = [
    path('', views.AiToTitle, name="AiToTitle"),
    re_path('^ajax/ajax_AiToTitle_Img/$', views.ajax_AiToTitle_Img, name="ajax_AiToTitle_Img"),
    re_path('^ajax/AjaxTitle/$', views.AjaxTitle, name="AjaxTitle"),
]