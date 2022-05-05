import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import *
from .forms import *
from registration.models import Student, Tutor
from tutor_area.models import *
from django.contrib.auth.models import User

NAME_BLOCK_UPGRADE = {
    'man': 'человек и общество',
    'economic': 'экономика',
}


def home(request):
    if request.user.is_authenticated:
        u = User.objects.get(username=request.user)
        if Student.objects.filter(user=u).exists():
            course = False
            if Student.objects.get(user=u).upgrade:
                course = True
            return render(request, 'student_area/home.html', {'course': course})
    return HttpResponseRedirect('/login')


def upgrade(request):
    if request.user.is_authenticated:
        u = User.objects.get(username=request.user)
        if Student.objects.filter(user=u).exists() and Student.objects.get(user=u).upgrade:
            return render(request, 'student_area/upgrade.html')
    return HttpResponseRedirect('/login')


def second_part(request, name_block):
    if request.user.is_authenticated:
        u = User.objects.get(username=request.user)
        h_s_p = HomeworkSecondPart.objects.filter(who_send=u)
        tutor_answer = ''
        if h_s_p.exists():
            send = True
            if h_s_p[0].status_check == 2:
                tutor_answer = CheckResult.objects.get(id_h_second_part=h_s_p[0].id)
        else:
            send = False

        if request.method == 'POST':
            s_p = SecondPart.objects.get(id=int(list(request.POST.keys())[1]))
            form = HomeworkSecondPartForm(request.POST, request.FILES)
            files = request.FILES.getlist('docfile')
            if form.is_valid():
                for f in files:
                    h = HomeworkSecondPart(who_send=u, second_part=s_p, answer=f, date=timezone.now(), status_check=1)
                    h.save()
                send = True
        return render(request, 'student_area/upgrade/second_part.html', {
            'name_block': name_block,
            'send': send,
            'h_s_p': h_s_p,
            'tutor_answer': tutor_answer,
        })
    return HttpResponseRedirect('/login')


def intro(request):
    return render(request, 'student_area/intro.html')


def settings(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    return render(request, 'student_area/settings.html')


# TODO: разбить на несколько функций
def lesson(request, name_block, num_lesson):
    message = ''
    u = User.objects.get(username=request.user)
    s = Student.objects.get(user=u)
    b = Block.objects.get(name=name_block)
    num_block = b.num_block
    l = Lesson.objects.get(what_block=b, num=num_lesson)
    test = Test.objects.get(what_lesson=l)
    themes = [i for i in test.what_lesson.theme.split(", ")]
    recent_res = list(Result.objects.filter(user_id=u.id, test_id=test.id))
    questions = list(test.question_set.all())
    quest_choice = {}
    for question in questions:
        choices = Choice.objects.get(question=question).text.splitlines()
        if len(choices) == 1:
            quest_choice[question] = {'photo': choices[0]}
        else:
            for i in range(len(choices)):
                choices[i] = "{}. {}".format(i + 1, choices[i])
            quest_choice[question] = {'text': choices}

    videos = l.video.split()

    if request.method == 'POST':
        if request.POST.get('end_lesson') == '':
            s.last_lesson_upgrade += 1
            s.save()
        else:
            user_points = 0
            max_points = 0
            result = Result(user=u, test=test, all_points=user_points, data_created=datetime.datetime.now())
            result.save()
            i = 0
            for answer in list(request.POST.keys())[1:-1]:
                user_point = 0
                q = questions[i]
                user_answer = request.POST[answer]
                a = Answer(user=u, question=q, choice=user_answer, result=result)
                a.save()
                i += 1

                question = Question.objects.get(what_test=Test.objects.get(num=num_lesson), number=int(answer))
                if Choice.objects.get(question=question).photo_or_not:
                    answer_int = [int(user_answer[i]) for i in range(len(user_answer))]
                    right_answer_int = [int(q.right_answer[i]) for i in range(len(q.right_answer))]
                else:
                    answer_int = sorted([int(user_answer[i]) for i in range(len(user_answer))])
                    right_answer_int = sorted([int(q.right_answer[i]) for i in range(len(q.right_answer))])

                # Подсчет баллов
                right_point = 0
                for k in right_answer_int:
                    if k in answer_int:
                        right_point += 1

                if right_point == len(right_answer_int) and right_point == len(answer_int):  # все верно
                    user_point = q.max_point
                elif right_point == len(right_answer_int) - 1 and len(answer_int) == len(right_answer_int):  # один неправильный
                    user_point = q.max_point - 1
                elif right_point == len(right_answer_int) - 1 and len(answer_int) == len(right_answer_int) - 1: # одного не хватает
                    user_point = q.max_point - 1
                elif right_point == len(right_answer_int) and len(answer_int) == len(right_answer_int) + 1:  # один лишний
                    user_point = q.max_point - 1
                else:
                    user_point = 0
                user_points += user_point
                max_points += q.max_point
                result.test.max_points = max_points
                result.test.save()
                e = EveryQuestionChoice(result_test=result, point=user_point, num_question=i, user_answer=user_answer   )
                e.save()
            result.all_points = user_points
            result.save()
            return HttpResponseRedirect('/test/upgrade/{}'.format(result.id))

    form = HomeworkForm()
    return render(request, 'student_area/upgrade/lesson.html', {
        'message': message,
        'form': form,
        'num_lesson': int(num_lesson),
        'name_block': name_block,
        'num_block': num_block,
        'videos': videos,  # ссылки на видео дня (список)
        'test': test,  # объект теста урока
        'quest_choice': quest_choice,  # {question: [choices]}
        'questions': questions,
        'num_question': [i for i in range(1, test.num_question + 1)],
        'recent_res': recent_res,
        'student': s,
        'themes': themes,
    })


def block(request, name_block):
    if request.user.is_authenticated:
        u = User.objects.get(username=request.user)
        if Student.objects.filter(user=u).exists():
            if Student.objects.get(user=u).upgrade:
                b = Block.objects.get(name=name_block)
                lessons = list(Lesson.objects.filter(what_block=b))
                last_lesson = Student.objects.get(user=u).last_lesson_upgrade
                num_lessons = [i for i in range(1, b.num_lessons + 1)]
                print(lessons)
                return render(request, 'student_area/upgrade/block.html', {
                    'title': NAME_BLOCK_UPGRADE[name_block],
                    'num_lessons': num_lessons,
                    'name_block': name_block,
                    'last_lesson': last_lesson,
                    'lessons': lessons,
                })
            return HttpResponseRedirect('/student_page')
    return HttpResponseRedirect('/login')

# class GetQuestion(GenericAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = QuestionSerializer
#     template_name = 'student_area/upgrade/test.html'
#
#     def get(self, request, format=None):
#         questions = Question.objects.filter(visible=True, )
#         last_point = QuestionSerializer(questions, many=True)
#         return Response(last_point.data)
#
#
# class QuestionAnswer(GenericAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = AnswerSerializer
#     template_name = 'student_area/upgrade/answer.html'
#
#     def post(self, request, format=None):
#         answer = AnswerSerializer(data=request.data, context=request)
#         if answer.is_valid(raise_exception=True):
#             answer.save()
#             return Response({'result': 'OK'})
