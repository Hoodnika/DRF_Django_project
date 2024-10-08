from django.contrib import admin

from userapp.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'id', 'last_login')
    list_filter = ('email', 'is_superuser')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'datetime_payment', 'price', 'paid_course', 'paid_lesson', 'payment_type', 'id')
    list_filter = ('price', 'owner',)
