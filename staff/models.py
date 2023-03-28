from django.contrib.auth import get_user_model
from django.db import models


class Employee(models.Model):
    tg_login = models.CharField(max_length=30, unique=True)
    work_status = models.BooleanField(default=True)
    chat = models.ForeignKey(
        'Chat',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.tg_login


class Chat(models.Model):
    name = models.CharField(max_length=30)
    chat_id = models.IntegerField(unique=True)
    tl = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name


class AwayLimit(models.Model):
    amount = models.PositiveIntegerField()
    chat = models.OneToOneField(
        'Chat',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Чат "{self.chat}": {self.amount}'
