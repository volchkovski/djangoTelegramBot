from django.contrib import admin
from .models import Employee, Chat, AwayLimit


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('tg_login', 'chat', 'work_status')


admin.site.register(Chat)
admin.site.register(AwayLimit)
