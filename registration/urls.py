from django.urls import re_path, include
from .views import *
from django.contrib import admin

urlpatterns = [
    re_path(r'admin/', admin.site.urls),
    re_path(r'login/', check_login, name="login"),
    re_path(r'logout/', logout_view, name='logout'),
    re_path(r'sign_up/', sign_up, name='sign_up'),
]
