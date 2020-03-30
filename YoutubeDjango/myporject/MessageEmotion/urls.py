from django.urls import path,re_path
from . import views
from django.conf.urls import url  #導入url套件
app_name='MessageEmotion'

from django.conf.urls import url, include
from django.contrib import admin
# app_name = 'blog'
urlpatterns = [
    path('', views.MessageEmotion, name="MessageEmotion"),
    re_path(r'^ajax/ajax_MessageEmotion/$', views.ajax_MessageEmotion, name="ajax_MessageEmotion"),
]