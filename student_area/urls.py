from django.urls import re_path
from django.conf.urls.static import static

from . import views
from site_school import settings

urlpatterns = [
    re_path(r'course_1/test/answer', views.QuestionAnswer.as_view()),
    re_path(r'course_1/test', views.GetQuestion.as_view()),
    re_path(r'course_1/1', views.lesson_1, name='send_homework'),
    re_path(r'course_1', views.course_1, name='course_1'),
    re_path(r'settings', views.settings, name='settings'),
    re_path(r'', views.home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
