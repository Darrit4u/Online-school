from django.urls import re_path
from django.conf.urls.static import static

from . import views
from site_school import settings

urlpatterns = [
    re_path(r'course_1/(?P<id_student>\w+)', views.student, name='detail'),
    re_path(r'course_1', views.course_1, name='course_1'),
    re_path(r'settings', views.settings_user, name='settings'),
    re_path(r'(\w+.*)', views.download_file, name='download_file'),
    re_path(r'^', views.home, name='home')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
