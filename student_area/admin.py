from django.contrib import admin

from .models import *

# TODO: переименовать в админке Homework object (n) в, например, ник отправляющего
admin.site.register(Homework)


class BlockAdmin(admin.ModelAdmin):
    list_display = (
        'num_lessons',
        'name',
        'visible'
    )


class TestAdmin(admin.ModelAdmin):
    list_display = (
        'what_block',
        'what_lesson',
        'num',
        'theme'
    )
    list_filter = ('what_block', )


class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'what_block',
        'num',
        'video',
    )


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'what_test',
        'num_task',
        'text',
        'max_point',
        'visible'
    )


class ChoiceAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'text',
        'right_or_not'
    )
    list_filter = ('question',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'question',
        'choice',
        'data_created',
    )
    list_filter = ('user',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Lesson, LessonAdmin)
