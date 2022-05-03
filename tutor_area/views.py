from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import FileResponse
import os
from django.contrib.auth.models import User

from registration.models import Student, Tutor
from student_area.models import *
from .models import *
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
    return render(request, 'student_area/intro.html')


def student(request, id_student):
    u = User.objects.get(id=id_student)
    if request.method == 'POST':
        if request.FILES.get('docfile'):
            files = request.FILES.getlist('docfile')
            h = list(dict(request.POST))[1]
            h = HomeworkSecondPart.objects.get(id=h)
            for f in files:
                tutor_answer = CheckResult(id_student=u, id_h_second_part=h.id, file_answer=f)
                tutor_answer.save()
                h.status_check = 2
                h.save()
        else:
            id_accept_result = list(dict(request.POST))[1]
            accept_result = Result.objects.get(id=id_accept_result)
            accept_result.status_check = 2
            accept_result.save()

    home_sec_part = HomeworkSecondPart.objects.filter(who_send=u)
    context_for_sec_part = {}
    for i in range(len(home_sec_part)):
        h = home_sec_part[i]
        context_for_sec_part[h] = h.second_part.theme

    h = Homework.objects.filter(who_send=User.objects.get(id=id_student))
    s = Student.objects.get(user=User.objects.get(id=id_student))
    task = set([Test.objects.get(id=t.num_task) for t in list(h)])

    content = {}
    for t in list(h):
        res = list(Result.objects.filter(user=u, test=Test.objects.get(id=t.num_task)))
        include = {}
        for r in range(len(res)):
            homework_with_one_home_id = h.filter(result_obj=res[r])
            include[res[r]] = [i.answer for i in list(homework_with_one_home_id)]

        content[Test.objects.get(id=t.num_task)] = include
    # content = {
    #    test.object: {
    #        result.obj: [files]
    #        }
    #    }

    result_all = list(set([i.result_obj for i in h]))
    context = {}
    for home_id in range(len(result_all)):
        homework_with_one_home_id = h.filter(result_obj=result_all[home_id])
        context[homework_with_one_home_id[0].result_obj] = ([i.answer for i in list(homework_with_one_home_id)])

    return render(request, 'tutor_area/student.html', {
        'homework': list(h),
        'task': task,
        'first_name_student': s.first_name,
        'last_name_student': s.last_name,
        'context': context,
        'h_sec_p': context_for_sec_part,
        'content': content
    })

# [ [file in homework with first_id_result], second_id_result ]


def download_file(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    response = HttpResponseRedirect('/login')
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
