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


class Question(models.Model):
    num_test = models.IntegerField(default=0)
    num_task = models.IntegerField(default=0)
    text = models.TextField()
    max_point = models.IntegerField(default=1)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return "{} вопрос {}".format(self.num_test, self.num_task)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    lock_other = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    choice = models.ForeignKey(Choice, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.choice.text
