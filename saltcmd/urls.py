"""saltcmd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from mycmd import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cmd/', views.cmd),
    url(r'^upload/', views.upload_file),
    url(r'^update/', views.update_file),
#    url(r'^dir/', views.dirDataJson),
    url(r'^dir/', views.update_files_salt),
    url(r'^index/', views.index_page),
    url(r'^general/', views.get_server_status),
    url(r'^login/', views.user_login),
    url(r'^data/', views.get_server_to_be_updated),
    url(r'^/', views.get_server_to_be_updated),
    url(r'^upload_script/',views.uploadify_script),
    url(r'^delete_uploadfile/$', views.profile_delte),
]
