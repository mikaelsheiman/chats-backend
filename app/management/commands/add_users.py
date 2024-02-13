from django.core.management import BaseCommand

from app.models import CustomUser


def add_users():
    CustomUser.objects.create_user(name='user', email='user@user.com', password='1234')
    CustomUser.objects.create_superuser(name='root', email='root@root.com', password='1234')

    for i in range(1, 3):
        CustomUser.objects.create_user(name=f'user{i}', email=f'user{i}@user.com', password='1234')

    for i in range(1, 3):
        CustomUser.objects.create_superuser(name=f'root{i}', email=f'root{i}@root.com', password='1234')

    print("Пользователи созданы")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users()

