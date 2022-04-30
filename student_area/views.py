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
from .forms import HomeworkForm
from registration.models import Student, Tutor
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
    return render(request, 'student_area/upgrade/second_part.html')


def demo(request):
    return render(request, 'student_area/demo.html')


def settings(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    return render(request, 'student_area/settings.html')


# TODO: разбить на несколько функций
def lesson(request, name_block, num_lesson):
    message = ''
    u = User.objects.get(username=request.user)
    b = Block.objects.get(name=name_block)
    num_block = b.num_block
    l = Lesson.objects.get(what_block=b, num=num_lesson)
    test = Test.objects.get(what_lesson=l)
    recent_res = list(Result.objects.filter(user_id=u.id, test_id=test.id))
    questions = list(test.question_set.all())
    quest_choice = {}
    for question in questions:
        quest_choice[question] = []
        for choice in list(question.choice_set.all()):
            quest_choice[question].append(choice)

    if request.method == 'POST':
        user_points = 0
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
            # Подсчет баллов
            answer_int = sorted([int(user_answer[i]) for i in range(len(user_answer))])
            right_answer_int = sorted([int(q.right_answer[i]) for i in range(len(q.right_answer))])
            right_point = 0
            for k in answer_int:
                if k in right_answer_int:
                    right_point += 1

            if right_point == len(right_answer_int):
                user_point = q.max_point
            elif right_point == len(right_answer_int) - 1:
                user_point = q.max_point - 1
            else:
                user_point = 0
            user_points += user_point
            e = EveryQuestionChoice(result_test=result, point=user_point, num_question=i)
            e.save()
        result.all_points = user_points
        result.save()
        return HttpResponseRedirect('/test/upgrade/{}'.format(result.id))

    form = HomeworkForm()
    return render(request, 'student_area/upgrade/lesson.html', {
        'message': message,
        'form': form,
        'num_lesson': num_lesson,
        'name_block': name_block,
        'num_block': num_block,
        'video': l.video,  # ссылки на видео дня
        'test': test,  # объект теста урока
        'quest_choice': quest_choice,  # {question: [choices]}
        'questions': questions,
        'num_question': [i for i in range(1, test.num_question+1)],
        'recent_res': recent_res,
    })


def block(request, name_block):
    if request.user.is_authenticated:
        u = User.objects.get(username=request.user)
        if Student.objects.filter(user=u).exists():
            if Student.objects.get(user=u).upgrade:
                b = Block.objects.get(name=name_block)
                last_lesson = Student.objects.get(user=u).last_lesson_upgrade
                num_lessons = [i for i in range(1, b.num_lessons+1)]
                return render(request, 'student_area/upgrade/block.html', {
                    'title': NAME_BLOCK_UPGRADE[name_block],
                    'num_lessons': num_lessons,
                    'name_block': name_block,
                    'last_lesson': last_lesson
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
