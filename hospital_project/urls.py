from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('his.urls')),  # his 앱의 URL 연결
]

if settings.DEBUG:  # DEBUG 모드에서만 static/media 파일 제공
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)