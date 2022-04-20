from django.db import models
from django.contrib.auth.models import User


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=600)
    last_name = models.CharField(max_length=600)
    email = models.EmailField()

    def __str__(self):
        return self.first_name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=600)
    last_name = models.CharField(max_length=600)
    email = models.EmailField()
    course_1 = models.BooleanField(default=False)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name
