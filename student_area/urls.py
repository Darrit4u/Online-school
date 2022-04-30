from django.urls import re_path
from django.conf.urls.static import static

from . import views
from site_school import settings

urlpatterns = [
    # re_path(r'upgrade/test/answer', views..as_view()),
    re_path(r'upgrade/(?P<user>\w+)/(?P<id_test>\d+)/result', views.get_result, name='result'),
    re_path(r'upgrade/(?P<name_block>\w+)/(?P<num_lesson>\d+)', views.lesson, name='send_homework'),
    re_path(r'upgrade/(?P<name_block>\w+)', views.block),
    re_path(r'upgrade', views.upgrade, name='upgrade'),
    re_path(r'demo', views.demo),
    re_path(r'settings', views.settings, name='settings'),
    re_path(r'', views.home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
