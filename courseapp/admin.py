from django.contrib import admin

from courseapp.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'id', 'updated_at')
    list_filter = ('title', )


@admin.register(Lesson)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'url', 'course', 'id', 'updated_at')
    list_filter = ('title', 'course',)

