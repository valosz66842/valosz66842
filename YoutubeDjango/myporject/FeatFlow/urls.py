from django.urls import path,re_path
from . import views
from django.conf.urls import url  #導入url套件
app_name='FeatFlow'

from django.conf.urls import url, include
from django.contrib import admin
# app_name = 'blog'


urlpatterns = [
    path('', views.FeatFlow, name="FeatFlow"),
    re_path(r'^ajax/featflow/$', views.ajax_featflow, name="ajax_featflow"),
]