from django.urls import path,re_path
from . import views
from django.conf.urls import url  #導入url套件
app_name='YoutubeFlow'

from django.conf.urls import url, include
from django.contrib import admin
# app_name = 'blog'


urlpatterns = [
    path('', views.YoutubeFlow, name="YoutubeFlow"),
    re_path(r'^ajax/youtube/$', views.ajax_youtube, name="ajax_youtube"),
    re_path(r'^ajax/youtubeImg/$', views.ajax_youtube_Img, name="ajax_youtube_Img")
]
