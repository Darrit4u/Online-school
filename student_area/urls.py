from django.urls import re_path
from django.conf.urls.static import static

from . import views
from site_school import settings

urlpatterns = [
    re_path(r'upgrade/intro', views.intro),
    re_path(r'upgrade/(?P<name_block>\w+)/secondpart', views.second_part),
    re_path(r'upgrade/(?P<name_block>\w+)/(?P<num_lesson>\d+)', views.lesson, name='send_homework'),
    re_path(r'upgrade/(?P<name_block>\w+)', views.block),
    re_path(r'upgrade', views.upgrade, name='upgrade'),
    re_path(r'settings', views.settings, name='settings'),
    re_path(r'', views.home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
