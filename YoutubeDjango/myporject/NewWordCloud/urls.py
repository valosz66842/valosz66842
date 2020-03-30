from django.urls import path,re_path
from . import views
from django.conf.urls import url  #導入url套件
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
app_name='NewWordCloud'


urlpatterns =[
    path('',views.NewWordCloud, name="NewWordCloud"),
    re_path(r'^ajax/ajax_NewWordCloud_Img/$', views.ajax_NewWordCloud_Img, name="ajax_NewWordCloud_Img"),
    re_path(r'^ajax/Json_Ajax/$',views.Json_Ajax,name="Json_Ajax")
]