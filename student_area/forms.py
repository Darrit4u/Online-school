from django import forms
from .models import Homework, SecondPart


class HomeworkForm(forms.ModelForm):
    docfile = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Homework
        fields = ['docfile']


class HomeworkSecondPartForm(forms.ModelForm):
    docfile = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = SecondPart
        fields = ['docfile']
# class AnswerForm(forms.ModelForm):
#     answers = forms.MultipleChoiceField()
#
#     class Meta:
#         model = Answer
#         fields = ['Answer']
