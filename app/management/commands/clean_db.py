from django.core.management.base import BaseCommand
from app.models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Message.objects.all().delete()
        Chat.objects.all().delete()
        CustomUser.objects.all().delete()