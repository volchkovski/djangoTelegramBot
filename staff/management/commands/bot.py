from typing import Optional

import telebot

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from staff.models import Chat, Employee, AwayLimit


class Command(BaseCommand):
    help = 'Бот для контроля перерывов'

    @staticmethod
    def get_chat(chat_id: int) -> Optional[Chat]:
        try:
            chat = Chat.objects.get(chat_id=chat_id)
        except ObjectDoesNotExist:
            return None
        return chat

    @staticmethod
    def get_employee(tg_login: str, chat: Chat) -> Optional[Employee]:
        try:
            employee = Employee.objects.get(tg_login=tg_login, chat=chat)
        except ObjectDoesNotExist:
            return None
        return employee

    @staticmethod
    def get_away_limit_amount(chat: Chat) -> Optional[int]:
        try:
            away_limit = AwayLimit.objects.get(chat=chat).amount
        except ObjectDoesNotExist:
            return None
        return away_limit

    def handle(self, *args, **kwargs):
        bot = telebot.TeleBot(
            settings.TG_TOKEN,
            parse_mode='markdown',
        )

        @bot.message_handler(commands=['away'])
        def go_away(message):
            chat_id = message.chat.id
            tg_login = message.from_user.username
            print('Get away from', tg_login)
            chat = self.get_chat(chat_id)
            if not chat:
                print(chat_id, 'is not added')
                bot.reply_to(message, 'Этот чат не был добавлен!')
                return

            employee = self.get_employee(tg_login, chat)
            if not employee:
                print(tg_login, 'is not added')
                bot.reply_to(message, 'Тебя не добавили в сотрудники этого чата!')
                return

            if employee.work_status == 'Отошел':
                text = ('Ты уже отходил. Возможно, хочешь вернуться к работе, '
                        'тогда воспользуся командой /here')
                bot.reply_to(message, text)
                return

            if employee.work_status == Employee.WorkStatus.DAY_OFF:
                text = ('По данным из космоса ты выходной. Возможно, хочешь вернуться к работе, '
                        'тогда воспользуся командой /here')
                bot.reply_to(message, text)
                return

            away_limit_amount = self.get_away_limit_amount(chat)
            if away_limit_amount is None:
                bot.reply_to(message, 'Для этого чата не настроен лимит сотрудников в перерыве.')
                return

            current_away = Employee.objects.filter(chat=chat, work_status='Отошел').count()
            if current_away == away_limit_amount:
                text = 'Максимальное количество сотрудников уже в перерыве. Дождись пока кто-то вернется к работе.'
                bot.reply_to(message, text)
                return

            employee.work_status = 'Отошел'
            employee.save()
            bot.reply_to(message, 'Понял-принял!')
            return

        @bot.message_handler(commands=['here'])
        def go_back(message):
            chat_id = message.chat.id
            tg_login = message.from_user.username
            print('Get here from', tg_login)
            chat = self.get_chat(chat_id)
            if not chat:
                print(chat_id, 'is not added')
                bot.reply_to(message, 'Этот чат не был добавлен!')
                return

            employee = self.get_employee(tg_login, chat)
            if not employee:
                print(tg_login, 'is not added')
                bot.reply_to(message, 'Тебя не добавили в сотрудники!')
                return

            if employee.work_status == 'Работает':
                text = ('Ты и так работаешь. Возможно, хочешь передохнуть, '
                        'тогда воспользуся командой /away')
                bot.reply_to(message, text)
                return

            employee.work_status = 'Работает'
            employee.save()
            bot.reply_to(message, 'Наконец-то!')
            return

        @bot.message_handler(commands=['dayoff'])
        def go_dayoff(message):
            chat_id = message.chat.id
            tg_login = message.from_user.username
            print('Get dayoff from', tg_login)
            chat = self.get_chat(chat_id)
            if not chat:
                print(chat_id, 'is not added')
                bot.reply_to(message, 'Этот чат не был добавлен!')
                return

            employee = self.get_employee(tg_login, chat)
            if not employee:
                print(tg_login, 'is not added')
                bot.reply_to(message, 'Тебя не добавили в сотрудники!')
                return

            if employee.work_status == Employee.WorkStatus.DAY_OFF:
                text = ('По данным из космоса ты выходной. Возможно, хочешь вернуться к работе, '
                        'тогда воспользуся командой /here')
                bot.reply_to(message, text)
                return

            employee.work_status = Employee.WorkStatus.DAY_OFF
            employee.save()
            bot.reply_to(message, 'Хороших выходных!)')
            return

        bot.infinity_polling()
