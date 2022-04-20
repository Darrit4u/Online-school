from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import FileResponse
import os
from django.contrib.auth.models import User

from registration.models import Student, Tutor
from student_area.models import Homework
from site_school import settings


def home(request):
    if request.user.is_authenticated:
        u = User.objects.get(username=request.user)
        if Tutor.objects.filter(user=u).exists():
            return render(request, 'tutor_area/home.html')
    return HttpResponseRedirect('/login')


def course_1(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    u = User.objects.get(username=request.user)
    t = Tutor.objects.get(user=u)
    if not t:
        return HttpResponseRedirect('/login')

    students = list(Student.objects.filter(tutor=t))
    return render(request, 'tutor_area/course_1.html', {'students': students})


def student(request, id_student):
    h = list(Homework.objects.filter(who_send=User.objects.get(username=id_student)))
    return render(request, 'tutor_area/s1.html', {'homework': h})


def download_file(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(content_type="application/octet-stream")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            response.write(fh.read())
    return response
    # recent_page = request.META.get('HTTP_REFERER')
    # return HttpResponseRedirect(recent_page)


def settings_user(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    return render(request, 'tutor_area/settings.html')
