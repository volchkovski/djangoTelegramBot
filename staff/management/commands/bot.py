import telebot

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from staff.models import Chat, Employee, AwayLimit


class Command(BaseCommand):
    help = 'Бот для контроля перерывов'

    def handle(self, *args, **kwargs):
        bot = telebot.TeleBot(
            settings.TG_TOKEN,
            parse_mode='markdown',
        )

        @bot.message_handler(commands=['away'])
        def get_away(message):
            chat_id = message.chat.id
            tg_login = message.from_user.username
            print('Get brb from', tg_login)
            try:
                chat = Chat.objects.get(chat_id=chat_id)
            except ObjectDoesNotExist:
                print(chat_id, 'is not added')
                bot.reply_to(message, 'Этот чат не был добавлен!')
                return

            try:
                employee = Employee.objects.get(tg_login=tg_login, chat=chat)
            except ObjectDoesNotExist:
                print(tg_login, 'is not added')
                bot.reply_to(message, 'Тебя не добавили в сотрудники этого чата!')
                return

            if not employee.work_status:
                text = ('Ты уже отходил. Возможно, хочешь вернуться к работе, '
                        'тогда воспользуся командой /here')
                bot.reply_to(message, text)
                return

            try:
                away_limit = AwayLimit.objects.get(chat=chat).amount
            except ObjectDoesNotExist:
                bot.reply_to(message, 'Для этого чата не настроен лимит сотрудников в перерыве.')
                return

            current_away = Employee.objects.filter(chat=chat, work_status=False).count()
            if current_away == away_limit:
                text = 'Максимальное количество сотрудников уже в перерыве. Дождись пока кто-то вернется к работе.'
                bot.reply_to(message, text)
                return

            employee.work_status = False
            employee.save()
            bot.reply_to(message, 'Понял-принял!')
            return

        @bot.message_handler(commands=['here'])
        def get_back(message):
            chat_id = message.chat.id
            tg_login = message.from_user.username
            print('Get here from', tg_login)
            try:
                Chat.objects.get(chat_id=chat_id)
            except ObjectDoesNotExist:
                print(chat_id, 'is not added')
                bot.reply_to(message, 'Этот чат не был добавлен!')
                return

            try:
                employee = Employee.objects.get(tg_login=tg_login)
            except ObjectDoesNotExist:
                print(tg_login, 'is not added')
                bot.reply_to(message, 'Тебя не добавили в сотрудники!')
                return

            if employee.work_status:
                text = ('Ты и так работаешь. Возможно, хочешь передохнуть, '
                        'тогда воспользуся командой /away')
                bot.reply_to(message, text)
                return

            employee.work_status = True
            employee.save()
            bot.reply_to(message, 'Наконец-то!')
            return

        bot.infinity_polling()
