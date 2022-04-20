from django import forms
from .models import Homework


class HomeworkForm(forms.ModelForm):
    docfile = forms.FileField()

    class Meta:
        model = Homework
        fields = ['docfile']
