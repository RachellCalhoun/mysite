from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^blog/?$', views.post_list, name='post_list'),
    path('post/new/', views.post_new, name='post_new'),
    re_path(r'^post/(?P<pk>\d+)/$', views.post_detail_redirect),  # Legacy pk URLs redirect to slug
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    path('upload-image/', views.upload_image, name='upload_image'),
]
