from django import forms
from .models import Homework, Answer


class HomeworkForm(forms.ModelForm):
    docfile = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Homework
        fields = ['docfile']


# class AnswerForm(forms.ModelForm):
#     answers = forms.MultipleChoiceField()
#
#     class Meta:
#         model = Answer
#         fields = ['Answer']
