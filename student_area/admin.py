from django.contrib import admin

from .models import *

# TODO: переименовать в админке Homework object (n) в, например, ник отправляющего
admin.site.register(Homework)


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'num_test',
        'num_task',
        'text',
        'max_point',
    )


class ChoiceAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'text',
    )
    list_filter = ('question',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'question',
        'choice',
        'created'
    )
    list_filter = ('user',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
