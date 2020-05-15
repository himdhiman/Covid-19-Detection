from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from app import views

urlpatterns = [
    path('', view = views.home, name = 'home')
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)