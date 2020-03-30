from django.urls import path,re_path
from . import views
from django.conf.urls import url  #導入url套件

app_name='myapp'

urlpatterns = [
    path('', views.index, name="index"),
    path('index/', views.index, name="index"),
    re_path('^ajax/ajax_index_Img/$', views.ajax_index_Img, name="ajax_index_Img"),
]
