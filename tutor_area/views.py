from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import FileResponse
import os
from django.contrib.auth.models import User

from registration.models import Student, Tutor
from student_area.models import *
from site_school import settings


def home(request):
    if request.user.is_authenticated:
        u = User.objects.get(username=request.user)
        if Tutor.objects.filter(user=u).exists():
            return render(request, 'tutor_area/home.html')
    return HttpResponseRedirect('/login')


def upgrade(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    u = User.objects.get(username=request.user)
    t = Tutor.objects.get(user=u)
    if not t:
        return HttpResponseRedirect('/login')

    students = list(Student.objects.filter(tutor=t))
    return render(request, 'tutor_area/upgrade.html', {'students': students})


def demo(request):
    return render(request, 'student_area/demo.html')


def student(request, id_student):
    h = list(Homework.objects.filter(who_send=User.objects.get(id=id_student)))
    task = set([Test.objects.get(id=t.num_task) for t in h])
    return render(request, 'tutor_area/student.html', {'homework': h, 'task': task})


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
