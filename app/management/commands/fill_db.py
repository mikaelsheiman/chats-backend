import random

from django.core import management
from django.core.management.base import BaseCommand
from app.models import *
from .utils import random_date, random_timedelta, random_text


def add_messages():
    users = CustomUser.objects.filter(is_superuser=False)
    moderators = CustomUser.objects.filter(is_superuser=True)

    if len(users) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    for _ in range(30):
        message = Message.objects.create()
        message.text = random_text(15)
        message.status = random.randint(2, 5)
        message.owner = random.choice(users)

        if message.status in [3, 4]:
            message.date_complete = random_date()
            message.date_formation = message.date_complete - random_timedelta()
            message.date_created = message.date_formation - random_timedelta()
            message.moderator = random.choice(moderators)
        else:
            message.date_formation = random_date()
            message.date_created = message.date_formation - random_timedelta()

        if message.status in [2, 3, 4]:
            message.check_spam = random.randint(0, 2)

        message.save()

    print("Заявки добавлены")


def add_chats():
    Chat.objects.create(
        name="Баскетбольная секция",
        users_count=53,
        image="chats/1.jpg"
    )

    Chat.objects.create(
        name="Кружок робототехники",
        users_count=112,
        image="chats/2.jpg"
    )

    Chat.objects.create(
        name="Аптека",
        users_count=78,
        image="chats/3.jpg"
    )

    Chat.objects.create(
        name="Новости о машинах",
        users_count=24,
        image="chats/4.jpg"
    )

    Chat.objects.create(
        name="Городской чат",
        users_count=11,
        image="chats/5.jpg"
    )

    chats = Chat.objects.all()
    messages = Message.objects.all()
    for message in messages:
        random.choice(chats).messages.add(message)

        for i in range(1, 3):
            message.chats.add(random.choice(chats))

    print("Услуги добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        management.call_command("clean_db")
        management.call_command("add_users")

        add_messages()
        add_chats()









