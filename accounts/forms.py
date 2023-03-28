from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import TeamLead


class TeamLeadCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = TeamLead
        fields = UserCreationForm.Meta.fields + ('tg_login',)


class TeamLeadChangeForm(UserChangeForm):

    class Meta:
        model = TeamLead
        fields = UserChangeForm.Meta.fields
