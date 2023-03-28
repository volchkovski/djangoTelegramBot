from django.contrib.auth.models import AbstractUser
from django.db import models


class TeamLead(AbstractUser):
    tg_login = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = 'Тимлид'
        verbose_name_plural = 'Тимлиды'
