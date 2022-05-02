from django.contrib import admin
from .models import *


class CheckResultAdmin(admin.ModelAdmin):
    list_display = (
        'id_student',
        'id_h_second_part',
        'file_answer'
    )


admin.site.register(CheckResult, CheckResultAdmin)
