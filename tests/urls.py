from django.urls import include, re_path

from .views import *

urlpatterns = [
    re_path(r'upgrade/(?P<id_result>\w+)/', get_result, name='result'),
]
