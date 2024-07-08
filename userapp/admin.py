from django.contrib import admin

from userapp.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', 'is_staff')
    list_filter = ('email', 'is_superuser')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime_payment', 'cost', 'paid_course', 'paid_lesson', 'payment_type')
    list_filter = ('cost', 'user',)
