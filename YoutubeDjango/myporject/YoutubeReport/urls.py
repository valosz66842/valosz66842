from django.urls import path, re_path
from . import views
from django.conf.urls import url  # 導入url套件

app_name = 'YoutubeReport'
urlpatterns = [
    path('', views.YoutubeReport, name="YoutubeReport"),
    re_path(r'^ajax/ajax_YoutubeReport_Img/$', views.ajax_YoutubeReport_Img, name="ajax_YoutubeReport_Img"),
    re_path(r'^ajax/ajax_Two_YoutubeReport_Img/$', views.ajax_Two_YoutubeReport_Img, name="ajax_Two_YoutubeReport_Img"),
]
