from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
import datetime

from student_area.models import *
from student_area.forms import HomeworkForm
from django.contrib.auth.models import User


def get_result(request, id_result):
    if request.user.is_authenticated:
        res = Result.objects.get(id=id_result)
        u = User.objects.get(id=res.user_id)
        test = Test.objects.get(id=res.test_id)
        num_lesson = test.what_lesson.num
        name_block = test.what_block.name
        questions = list(test.question_set.all())
        quest_choice = {}
        user_choices = EveryQuestionChoice.objects.filter(result_test=res)
        for question in questions:
            choices = Choice.objects.get(question=question).text.splitlines()
            if len(choices) == 1:
                quest_choice[question] = {'photo': choices[0]}
            else:
                for i in range(len(choices)):
                    choices[i] = "{}. {}".format(i + 1, choices[i])
                quest_choice[question] = {'text': choices}

        if request.method == 'POST':
            form = HomeworkForm(request.POST, request.FILES)
            files = request.FILES.getlist('docfile')
            if form.is_valid():
                for f in files:
                    h = Homework(who_send=u, answer=f, date=timezone.now(), num_task=test.id, result_obj=res)
                    h.save()
                    res.status_check = 1
                    res.save()
        return render(request, 'student_area/upgrade/result.html', {
            'message': res.status_check,
            'user_choices': user_choices,
            'test': test,  # объект теста урока
            'u': u,
            'res': res,
            'videos': test.what_lesson.video.split(),
            'num_lesson': num_lesson,
            'num_block': test.what_block.num_block,
            'name_block': name_block,
            'quest_choice': quest_choice,  # {question: [choices]}
            'questions': questions,
            'num_question': [i for i in range(1, test.num_question+1)],
        })
    return HttpResponseRedirect('/login')

