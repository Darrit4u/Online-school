from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import Homework, Question, Choice, Answer
from .forms import HomeworkForm
from registration.models import Student, Tutor
from django.contrib.auth.models import User


def home(request):
    if request.user.is_authenticated:
        u = User.objects.get(username=request.user)
        if Student.objects.filter(user=u).exists():
            course = False
            if Student.objects.get(user=u).course_1:
                course = True
            return render(request, 'student_area/home.html', {'course': course})
    return HttpResponseRedirect('/login')


def course_1(request):
    if request.user.is_authenticated:
        u = User.objects.get(username=request.user)
        if Student.objects.filter(user=u).exists() and Student.objects.get(user=u).course_1:
            return render(request, 'student_area/course_1.html')
    return HttpResponseRedirect('/login')


def settings(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    return render(request, 'student_area/settings.html')


# TODO: предача номера урока через get в url и распаковка в одной функции.
# TODO: Функция принимает аргумент и рендерит нужный html
# ! чел не может отправить сразу еще один файл. но если он перезайдет на страницу, то сможет
def lesson_1(request):
    message = False
    if request.method == 'POST':
        form = HomeworkForm(request.POST, request.FILES)
        if form.is_valid():
            u = User.objects.get(username=request.user)
            h = Homework(who_send=u, answer=request.FILES['docfile'], date=timezone.now(), num_task=1)
            h.save()
            message = True
    else:
        form = HomeworkForm()
    return render(request, 'student_area/course_1/1.html', {'message': message, 'form': form})


def get_question(request, num_test):
    questions = list(Question.objects.filter(num_test=num_test))  # список всех вопрос в тесте
    if Answer.objects.filter(question=questions[0]).exists():
        return render(request, 'student_area/course_1/result.html', {})
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        all_points = 0
        errors = {}
        for question in questions:
            choices = request.POST.getlist('choice')
            question_points = 0
            for choice in choices:
                c = Choice.objects.get(id=int(choice))
                user_answer = Answer(user=user, question=question, choice=c, data_created=timezone.now())
                user_answer.save()
                if c.right_or_not:
                    all_points += 1
                    question_points += 1
            if question_points < question.max_point:
                errors[question.id] = question_points
        return render(request, 'student_area/course_1/result.html', {
            'questions': questions,
            'all_points': all_points,
            'errors': errors
        })
    return render(request, 'student_area/course_1/test.html', {'questions': questions})


def get_result(request, num_test):
    pass

# class GetQuestion(GenericAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = QuestionSerializer
#     template_name = 'student_area/course_1/test.html'
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
#     template_name = 'student_area/course_1/answer.html'
#
#     def post(self, request, format=None):
#         answer = AnswerSerializer(data=request.data, context=request)
#         if answer.is_valid(raise_exception=True):
#             answer.save()
#             return Response({'result': 'OK'})
