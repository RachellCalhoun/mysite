from django.urls import include, re_path
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^',include('blog.urls')),
    re_path(r'^',include('projects.urls')),
    re_path(r'^tinymce/', include('tinymce.urls')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
