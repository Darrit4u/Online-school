from django.db import models
from django.contrib.auth.models import User


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=600)
    last_name = models.CharField(max_length=600)
    email = models.CharField(max_length=600)
    
    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=600)
    last_name = models.CharField(max_length=600)
    email = models.CharField(max_length=600)
    upgrade = models.BooleanField(default=False)
    last_lesson_upgrade = models.IntegerField(default=0)
    last_block_upgrade = models.IntegerField(default=1)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
