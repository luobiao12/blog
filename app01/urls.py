from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from blog import settings

from app01 import views

urlpatterns = [

    #后台管理
    url("(?P<username>\w+)/add_article",views.add_article),
    url(r"^poll", views.poll),
    url(r"^comment/$", views.comment),
    url(r"^get_comment_tree/(\d+)$", views.get_comment_tree),
    url(r"^(?P<username>\w+)/(?P<condition>(cate|tag|date))/(?P<params>\w+)", views.homesite),# home_site(username="wupeiqi")
    url(r"^(?P<username>\w+)/articles/(?P<article_id>\d+)", views.article_detail),# home_site(username="wupeiqi")

    url(r"^(?P<username>\w+)", views.homesite),  # home_site(request,username="wupeiqi")


]
