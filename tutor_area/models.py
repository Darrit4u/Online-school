from django.db import models
from django.contrib.auth.models import User

from student_area.models import *


class CheckResult(models.Model):
    id_student = models.ForeignKey(User, on_delete=models.CASCADE)
    id_h_second_part = models.IntegerField()  # id второй части, на которую отвечают
    file_answer = models.FileField(upload_to='tutor_answer/')
