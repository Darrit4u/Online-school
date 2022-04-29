from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.models import Group

from .models import Student, Tutor


def check_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            u = User.objects.get(username=request.user)
            if Student.objects.filter(user=u).exists():
                return HttpResponseRedirect('/student_page')
            elif Tutor.objects.filter(user=u).exists():
                return HttpResponseRedirect('/tutor_page')
            elif User.groups.filter(name='Admin'):
                return HttpResponseRedirect('/admin')
            else:
                return HttpResponse('Ошибка. Обратитесь в поддержку')

        else:
            error_message = "Неправильное имя пользователя или пароль"
            return render(request, 'registration/login.html', {"error_message": error_message})
    else:
        return render(request, 'registration/login.html', {"error_message": ""})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'registration/logout.html')
    return HttpResponseRedirect('/login')


def sign_up(request):
    context = {'error': []}
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if User.objects.filter(username=username).exists():
            context['error'].append('Такое имя пользователя уже есть, пожалуйста, выберите другое.')
        if User.objects.filter(email=email).exists():
            context['error'].append('Аккаунт с такой почтой уже существует!')
        if password != password2:
            context['error'].append('Пароли не совпадают. Будьте аккуратнее')
        else:
            if password == password2:
                User.objects.create_user(username, email, password)
                user = User.objects.get(username=username)
                tutor = Tutor.objects.get(user=User.objects.get(username='tutor'))
                s = Student(user=user, first_name=firstname, last_name=lastname, email=email, course_1=False, tutor=tutor)
                s.save()
                return HttpResponseRedirect('/login')
    return render(request, 'registration/sign_up.html', context)
