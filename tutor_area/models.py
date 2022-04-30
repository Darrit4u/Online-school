from django.db import models
from django.contrib.auth.models import User

from student_area.models import *


class CheckResult(models.Model):
    id_student = models.ForeignKey(User, on_delete=models.CASCADE)
    num_result = models.IntegerField()  # id результата ученика, на который отвечают
    file_answer = models.FileField(upload_to='')
