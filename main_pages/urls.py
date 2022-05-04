from django.urls import re_path
from django.conf.urls.static import static

from . import views
from site_school import settings

urlpatterns = [
    re_path(r'about', views.about, name='about'),
    re_path(r'schedule', views.schedule, name='schedule'),
    re_path(r'product', views.product, name='product'),
    re_path(r'feedback', views.feedback, name='feedback'),
    re_path(r'^$', views.index, name='index')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

