from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import TeamLeadCreationForm, TeamLeadChangeForm
from .models import TeamLead


class TeamLeadAdmin(UserAdmin):
    add_form = TeamLeadCreationForm
    form = TeamLeadChangeForm
    model = TeamLead
    list_display = ['username', 'tg_login', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('tg_login',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('tg_login',)}),
    )


admin.site.register(TeamLead, TeamLeadAdmin)
