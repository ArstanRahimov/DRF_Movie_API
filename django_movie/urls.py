from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .yasg import urlpatterns as doc_urls

from django_movie import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('account.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/v1/', include('movies.urls')),
]

urlpatterns += doc_urls  # добавляем url от swagger

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
