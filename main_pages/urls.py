from django.urls import re_path
from django.conf.urls.static import static

from . import views
from site_school import settings

urlpatterns = [
    re_path(r'', views.about, name='about'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

