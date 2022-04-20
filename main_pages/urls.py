from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'about', views.about, name='about'),
    re_path(r'schedule', views.schedule, name='schedule'),
    re_path(r'product', views.product, name='product'),
    re_path(r'feedback', views.feedback, name='feedback'),
    re_path(r'^$', views.index, name='index')
]
