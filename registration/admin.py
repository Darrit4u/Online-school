from django.contrib import admin

from .models import Student, Tutor

class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'first_name',
        'last_name',
        'email',
        'upgrade',
        'tutor',
        'last_lesson_upgrade'
        )

admin.site.register(Student, StudentAdmin)
admin.site.register(Tutor)
