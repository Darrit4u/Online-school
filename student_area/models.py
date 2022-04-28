from django.db import models
from django.contrib.auth.models import User
import os


# TODO: Возможно, добавить метод сортировки по нику отправляющего и дате
class Homework(models.Model):
    who_send = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    num_task = models.IntegerField(default=0)
    answer = models.FileField(upload_to='')
    date = models.DateField()

    def __str__(self):
        return self.who_send.username


class Block(models.Model):
    num_lessons = models.IntegerField()
    name = models.CharField(max_length=200)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    what_block = models.ForeignKey(Block, on_delete=models.CASCADE)
    num = models.IntegerField(default=0)
    video = models.CharField(max_length=200)

    def __str__(self):
        return "{} {}".format(self.what_block, self.num)


class Test(models.Model):
    what_block = models.ForeignKey(Block, on_delete=models.CASCADE)
    what_lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)
    num = models.IntegerField(default=0)
    num_question = models.IntegerField(default=0)
    theme = models.CharField(max_length=500)

    def __str__(self):
        return "{} {}".format(self.what_block, self.num)


class Question(models.Model):
    what_test = models.ForeignKey(Test, on_delete=models.CASCADE, default=1)
    num_task = models.IntegerField(default=0)
    text = models.TextField()
    max_point = models.IntegerField(default=1)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return "Тест {} вопрос {}".format(self.what_test.theme, self.num_task)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    lock_other = models.BooleanField(default=False)
    right_or_not = models.BooleanField(default=None)

    def __str__(self):
        return self.text


# Ответ пользователя (каждый выбор = одной модели)
class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    choice = models.ForeignKey(Choice, on_delete=models.DO_NOTHING)
    data_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.choice.text


# class Result(models.Model):
#     user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
#     question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
#     all_points = models.IntegerField()
#     answers = models.ForeignKey(Answer, on_delete=models.DO_NOTHING)
