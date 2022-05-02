from django.db import models
from django.contrib.auth.models import User
import os


class Block(models.Model):
    num_block = models.IntegerField(default=0)  # номер блока
    num_lessons = models.IntegerField()
    name = models.CharField(max_length=200)
    readable_name = models.CharField(max_length=500)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    what_block = models.ForeignKey(Block, on_delete=models.CASCADE)
    num = models.IntegerField(default=0)
    video = models.CharField(max_length=1000)
    theme = models.CharField(max_length=1000, default=0)

    def __str__(self):
        return "{} {}".format(self.what_block, self.num)


class Test(models.Model):
    what_block = models.ForeignKey(Block, on_delete=models.CASCADE)
    what_lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)
    num = models.IntegerField(default=0)  # номер теста
    num_question = models.IntegerField(default=0)  # кол-во вопросов
    theme = models.CharField(max_length=500)  # 1.1 1.2 1.4 нпр

    def __str__(self):
        return "{} {}".format(self.what_block, self.num)


class Question(models.Model):
    what_test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.TextField()
    max_point = models.IntegerField(default=1)
    number = models.IntegerField(default=0)
    visible = models.BooleanField(default=False)
    right_answer = models.CharField(max_length=200, default='')

    def __str__(self):
        return "Тест {} вопрос {}".format(self.what_test.theme, self.number)


class Choice(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    text = models.TextField()
    # lock_other = models.BooleanField(default=False)
    # right_or_not = models.BooleanField(default=None)
    photo_or_not = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    all_points = models.IntegerField()
    data_created = models.DateTimeField()
    status_check = models.IntegerField(default=0)  # статус проверки куратором

    def __str__(self):
        return "{} {} {}".format(self.user, self.test, self.all_points)


class EveryQuestionChoice(models.Model):
    result_test = models.ForeignKey(Result, on_delete=models.CASCADE)
    point = models.IntegerField(default=-1)
    num_question = models.IntegerField(default=0)
    user_answer = models.CharField(max_length=500)


# Ответ пользователя
class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    choice = models.CharField(max_length=200)
    result = models.ForeignKey(Result, on_delete=models.DO_NOTHING, default=0)

    def __str__(self):
        return "{} отправил ответ на {}".format(self.user, self.question)


# TODO: Возможно, добавить метод сортировки по нику отправляющего и дате
class Homework(models.Model):
    who_send = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    num_task = models.IntegerField(default=0)  # id теста, в ответ на который были присланы файлы
    result_obj = models.ForeignKey(Result, on_delete=models.CASCADE)  # по какому результату рно
    answer = models.FileField(upload_to='')
    date = models.DateField()

    def __str__(self):
        return self.who_send.username


class SecondPart(models.Model):
    theme = models.CharField(max_length=500, default=0)
    path_to_task = models.CharField(max_length=500)  # файл задания
    path_to_key = models.CharField(max_length=500)  # файл с ключами к заданию
    date_open = models.DateField()  # когда открывается новая вторая часть
    date_up_key = models.DateField()  # дедлайн


class HomeworkSecondPart(models.Model):
    who_send = models.ForeignKey(User, on_delete=models.CASCADE)
    second_part = models.ForeignKey(SecondPart, on_delete=models.CASCADE)
    answer = models.FileField(upload_to='second_part/')
    date = models.DateField()
    status_check = models.IntegerField(default=0)
