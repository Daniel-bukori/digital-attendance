from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('digital_attendance.urls')), # Inasoma njia zote kutoka app ya core
]

# Inaruhusu Django kusoma mafaili (vyeti na materials) wakati wa development/testing
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)