from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Employee(models.Model):

    class WorkStatus(models.TextChoices):
        WORK = 'Работает', 'Работает'
        AWAY = 'Отошел', 'Отошел'
        DAY_OFF = 'Выходной', 'Выходной'

    tg_login = models.CharField(max_length=30, unique=True)
    work_status = models.CharField(
        max_length=10,
        choices=WorkStatus.choices,
        default=WorkStatus.WORK,
    )
    chat = models.ForeignKey(
        'Chat',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.tg_login

    def get_absolute_url(self):
        return reverse('employees', args=[str(self.chat.pk)])


class Chat(models.Model):
    name = models.CharField(max_length=30)
    chat_id = models.IntegerField(unique=True)
    tl = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('chats')


class AwayLimit(models.Model):
    amount = models.PositiveIntegerField()
    chat = models.OneToOneField(
        'Chat',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Чат "{self.chat}": {self.amount}'
