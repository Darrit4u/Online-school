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
        'number',
        'text',
        'max_point',
        'visible',
        'right_answer'
    )
    list_filter = ('what_test', 'number')


class ChoiceAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'text',
        'number'
    )
    list_filter = ('question',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'question',
        'choice',
        # 'result'
    )
    list_filter = ('user',)


class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'test',
        'all_points',
        'data_created',
        'status_check'
    )


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Result, ResultAdmin)
