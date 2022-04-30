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


def demo(request):
    return render(request, 'student_area/demo.html')


def settings(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    return render(request, 'student_area/settings.html')


# TODO: предача номера урока через get в url и распаковка в одной функции.
# TODO: Функция принимает аргумент и рендерит нужный html
# ! чел не может отправить сразу еще один файл. но если он перезайдет на страницу, то сможет
def lesson(request, name_block, num_lesson):
    message = False
    u = User.objects.get(username=request.user)
    b = Block.objects.get(name=name_block)
    l = Lesson.objects.get(what_block=b, num=num_lesson)
    test = Test.objects.get(what_lesson=l)
    questions = list(test.question_set.all())
    quest_choice = {}
    for question in questions:
        quest_choice[question] = []
        for choice in list(question.choice_set.all()):
            quest_choice[question].append(choice)

    if Result.objects.filter(user=u, test=test).exists():
        return HttpResponseRedirect('/test/upgrade/{}/{}/result'.format(request.user, test.id))

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
        return HttpResponseRedirect('/test/upgrade/{}/{}/result'.format(request.user, test.id))

    form = HomeworkForm()
    return render(request, 'student_area/upgrade/lesson.html', {
        'message': message,
        'form': form,
        'num_lesson': num_lesson,
        'name_block': name_block,
        'video': l.video,  # ссылки на видео дня
        'test': test,  # объект теста урока
        'quest_choice': quest_choice,  # {question: [choices]}
        'questions': questions,
        'num_question': [i for i in range(1, test.num_question+1)],
    })


def send_file(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST, request.FILES)
        if form.is_valid():
            u = User.objects.get(username=request.user)
            h = Homework(who_send=u, answer=request.FILES['docfile'], date=timezone.now(), num_task=1)
            h.save()
            message = True
    else:
        form = HomeworkForm()


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


# def get_question(request, num_test):
#     questions = list(Question.objects.filter(num_test=num_test))  # список всех вопрос в тесте
#     if Answer.objects.filter(question=questions[0]).exists():
#         return render(request, 'student_area/upgrade/result.html', {})
#     if request.method == 'POST':
#         user = User.objects.get(username=request.user)
#         all_points = 0
#         errors = {}
#         for question in questions:
#             choices = request.POST.getlist('choice')
#             question_points = 0
#             for choice in choices:
#                 c = Choice.objects.get(id=int(choice))
#                 user_answer = Answer(user=user, question=question, choice=c, data_created=timezone.now())
#                 user_answer.save()
#                 if c.right_or_not:
#                     all_points += 1
#                     question_points += 1
#             if question_points < question.max_point:
#                 errors[question.id] = question_points
#         return render(request, 'student_area/upgrade/result.html', {
#             'questions': questions,
#             'all_points': all_points,
#             'errors': errors
#         })
#     return render(request, 'student_area/upgrade/test.html', {'questions': questions})

def get_result(request, user, id_test):
    if request.user.is_authenticated:
        u = User.objects.get(username=user)
        test = Test.objects.get(id=id_test)
        num_lesson = test.what_lesson.num
        questions = list(test.question_set.all())
        quest_choice = {}
        res = Result.objects.get(user_id=u.id, test_id=test.id)
        user_choices = EveryQuestionChoice.objects.filter(result_test=res)
        for question in questions:
            quest_choice[question] = []
            for choice in list(question.choice_set.all()):
                quest_choice[question].append(choice)

        if request.method == 'POST':
            form = HomeworkForm(request.POST, request.FILES)
            files = request.FILES.getlist('docfile')
            if form.is_valid():
                for f in files:
                    h = Homework(who_send=u, answer=f, date=timezone.now(), num_task=test.id)
                    h.save()
        return render(request, 'student_area/upgrade/result.html', {
            'user_choices': user_choices,
            'test': test,  # объект теста урока
            'u': u,
            'res': res,
            'video': test.what_lesson.video,
            'num_lesson': num_lesson,
            'quest_choice': quest_choice,  # {question: [choices]}
            'questions': questions,
            'num_question': [i for i in range(1, test.num_question+1)],
        })
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
