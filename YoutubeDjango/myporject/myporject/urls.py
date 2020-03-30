"""myporject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include,re_path
from django.conf.urls import url
from myapp.views import index
from django.views.generic import TemplateView


urlpatterns = {
    path('', include("myapp.urls")),
    path('index/', include("myapp.urls")),
    path('YoutubeFlow/', include('YoutubeFlow.urls')),
    path('AiToTitle/', include('AiToTitle.urls')),
    path('FeatFlow/', include('FeatFlow.urls')),
    path('MessageEmotion/', include('MessageEmotion.urls')),
    path('NewWordCloud/', include('NewWordCloud.urls')),
    path('YoutubeReport/', include('YoutubeReport.urls')),
}