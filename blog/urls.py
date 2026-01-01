from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^blog$', views.post_list, name='post_list'),
    re_path(r'^blog/$', views.post_list, name='post_list'),
    re_path(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    re_path(r'^post/new/$', views.post_new, name='post_new'),
    re_path(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    re_path(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    re_path(r'^post/(?P<pk>[0-9]+)/publish/$', views.post_publish, name='post_publish'),
    re_path(r'^post/(?P<pk>[0-9]+)/remove/$', views.post_remove, name='post_remove'),
    re_path(r'^comment/(?P<pk>[0-9]+)/approve/$', views.comment_approve, name='comment_approve'),
    re_path(r'^comment/(?P<pk>[0-9]+)/remove/$', views.comment_remove, name='comment_remove'),
    re_path(r'^upload-image/$', views.upload_image, name='upload_image'),
]
