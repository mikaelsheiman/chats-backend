# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
import datetime


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

# --- Мои Таблицы --- #

class ActiveManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().exclude(state=0)
    

class Managable(models.Model):
    objects = models.Manager()
    active_objects = ActiveManager()

    def logic_delete(self):
        self.state = 0
        self.save()

    class Meta:
        abstract = True


# Referenced as "user" in all other models; extends default User from django auth 
class Client(Managable):

    class State(models.IntegerChoices):
        DELETED = 0, _('Deleted') # deleted is zero so you can use if(obj.state)
        ACTIVE = 1, _('Active')

    auth_user = models.OneToOneField(User, models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=31)

    # Managable
    state = models.IntegerField(choices=State.choices, default=State.ACTIVE)
    
    def __str__(self) -> str:
        return f'Client ({self.id}) "{self.nickname}" {self.State.names[self.state]}'

    class Meta:
        db_table = 'client'


class Chat(Managable):
    
    class State(models.IntegerChoices):
        DELETED = 0, _('Deleted') # deleted is zero so you can use if(obj.state)
        ACTIVE = 1, _('Active')

    name = models.CharField(max_length=255)
    image = models.ImageField(null=True)
    clients = models.ManyToManyField(Client, through='ChatClients')
    messages = models.ManyToManyField('Message')
    last_update_time = models.DateTimeField(null=True, blank=True)
    # Managable
    state = models.IntegerField(choices=State.choices, default=State.ACTIVE)
    # messages_total = models.BigIntegerField(default=0, blank=True)
    # last_message = models.OneToOneField('Message', models.DO_NOTHING, null=True, related_name='chat_if_last_message')
    

    def __str__(self) -> str:
        return f'Chat ({self.id}) "{self.name}" {self.State.names[self.state]}'

    # def mes_inc(self):
    #     self.messages_total += 1
    #     self.save()
    #     return self
    
    # def mes_dec(self):
    #     self.messages_total -= 1
    #     self.save()
    #     return self

    @property
    def get_image(self):
        if self.image is not None:
            return self.image
        else:
            return None

    def set_update_time(self, time):
        self.last_update_time = time
        self.save()
    
    def set_update_time_now(self):
        self.last_update_time = datetime.datetime.now()
        self.save()

    def is_admin(self, client):
        return ChatClients.objects.get(client=client, chat=self).is_admin

    @property
    def messages_count(self):
        return self.messages.all().count()

    @property
    def members_count(self):
        return self.clients.all().count()
    
    @property
    def last_message(self):
        return Message.objects.filter(chat=self).order_by('-datetime').first()

    class Meta:
        db_table = 'chat'


class ChatClients(models.Model):
    chat = models.ForeignKey(Chat, models.CASCADE)
    client = models.ForeignKey(Client, models.CASCADE)
    is_admin = models.BooleanField(default=False, blank=True)
    read_messages = models.BigIntegerField(default=0, blank=True)

    def update_read_messages(self):
        self.read_messages = self.chat.messages_count
        self.save()
        return self
    
    def set_admin(self, is_admin):
        self.is_admin = is_admin
        self.save()
    
    @property
    def unread_messages(self):
        a = self.chat.messages_count - self.read_messages
        return a if a > 0 else 0

    class Meta:
        db_table = 'chat_clients'
        unique_together = (('chat', 'client'),)


class MessageManager(models.Manager):
    def create(self, **kwargs: Any) -> Any:
        m = super().create(**kwargs)
        kwargs['chats'].set_update_time(self.last().datetime)
        return m


class Message(Managable):

    class State(models.IntegerChoices):
        DELETED = 0, _('Deleted') # deleted is zero so you can use if(obj.state == 0)
        SENT = 1, _('Sent')
        DRAFT = 2, _('Draft')
        REJECTED = 3, _('Rejected')

    client = models.ForeignKey(Client, models.DO_NOTHING)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True)
    # Managable
    state = models.IntegerField(choices=State.choices, default=State.SENT)

    # chat = models.ForeignKey(Chat, models.CASCADE, related_name='messages')
    # is_reply = models.BooleanField(default=False, blank=True)
    # replyed_message = models.ForeignKey('Message', models.DO_NOTHING, null=True, blank=True)


    objects = MessageManager()

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'message'