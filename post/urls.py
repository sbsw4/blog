#coding=utf-8

from django.conf.urls import url
import views

urlpatterns=[
    url(r'^$',views.queryAll),
    url(r'^page/(\d+)$',views.queryAll),
    url(r'^post/(\d+)$',views.detail),
    url(r'^category/(\d+)$',views.queryPostByCid),
    url(r'^archive/(\d+)/(\d+)$',views.queryPostByCreated),
    url(r'^stream_video/', views.stream_video),
    url(r'^video/$',views.video),
]