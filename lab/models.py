# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from typing import Any
from django.db import models
from django.contrib.auth.models import User as AUser
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

import psycopg2 # ПОТОМ УДАЛИТЬ


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

    class ClientState(models.IntegerChoices):
        DELETED = 0, _('Deleted') # deleted is zero so you can use if(obj.state)
        ACTIVE = 1, _('Active')

    auth_user = models.OneToOneField(AUser, models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=31)

    state = models.IntegerField(choices=ClientState.choices, default=ClientState.ACTIVE)
    
    def __str__(self) -> str:
        return f'Client ({self.id}) "{self.nickname}" {self.ClientState.names[self.state]}'

    # ПОТОМ УДАЛИТЬ
    def get_table_name(self):
        return 'users'

    class Meta:
        db_table = 'users'


class Chat(Managable):
    class ChatState(models.IntegerChoices):
        DELETED = 0, _('Deleted') # deleted is zero so you can use if(obj.state)
        ACTIVE = 1, _('Active')

    name = models.CharField(max_length=255)
    messages = models.ManyToManyField("Message", null=True, related_name="chats")
    image_path = models.CharField(max_length=255, default='vector/dialog-svgrepo-com.svg', blank=True, null=True)
    users = models.ManyToManyField(Client, through='ChatUser')
    messages_total = models.BigIntegerField(default=0, blank=True)
    state = models.IntegerField(choices=ChatState.choices, default=ChatState.ACTIVE)
    # last_message = models.OneToOneField('Message', models.DO_NOTHING, null=True, related_name='chat_if_last_message')
    last_message_time = models.TimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f'Chat ({self.id}) "{self.name}" {self.ChatState.names[self.state]}'

    def mes_inc(self):
        self.messages_total += 1
        self.save()
        return self
    
    def mes_dec(self):
        self.messages_total -= 1
        self.save()
        return self

    def last_message_time_update(self, time):
        self.last_message_time = time
        self.save()

    @property
    def members_count(self):
        return self.users.all().count()
    
    @property
    def last_message(self):
        return Message.objects.filter(chat=self).order_by('-time').first()
    
    # ПОТОМ УДАЛИТЬ
    def get_table_name(self):
        return 'chats'

    class Meta:
        db_table = 'chats'


class ChatUser(models.Model):
    chat = models.ForeignKey(Chat, models.CASCADE)  # The composite primary key (chat_id, user_id) found, that is not supported. The first column is selected.
    user = models.ForeignKey(Client, models.CASCADE)
    is_admin = models.BooleanField(default=False, blank=True)
    read_messages = models.BigIntegerField(default=0, blank=True)

    def update_read_messages(self):
        self.read_messages = self.chat.messages_total
        self.save()
        return self
    
    @property
    def unread_messages(self):
        return self.chat.messages_total - self.read_messages

    class Meta:
        db_table = 'chat_user'
        unique_together = (('chat', 'user'),)


class MessageManager(models.Manager):
    def create(self, **kwargs: Any) -> Any:
        m = super().create(**kwargs)
        kwargs['chat'].mes_inc()
        kwargs['chat'].last_message_time_update(self.last().time)
        return m


class Message(Managable):

    class MessageState(models.IntegerChoices):
        DELETED = 0, _('Deleted') # deleted is zero so you can use if(obj.state)
        SENT = 1, _('Sent')
        DRAFT = 2, _('Draft')
        IN_PROCESS = 3, _('In process')
        REJECTED = 4, _('Rejected')


    chat = models.ForeignKey(Chat, models.CASCADE, null=True)
    user = models.ForeignKey(Client, models.DO_NOTHING)
    # message_state = models.ForeignKey(MessageState, models.DO_NOTHING)
    text = models.TextField(blank=True, null=True)
    time = models.TimeField(auto_now_add=True, blank=True)
    is_reply = models.BooleanField(default=False, blank=True)
    replyed_message_id = models.BigIntegerField(blank=True, null=True)
    state = models.IntegerField(choices=MessageState.choices, default=MessageState.SENT)

    objects = MessageManager()

    # ПОТОМ УДАЛИТЬ
    def get_table_name(self):
        return 'messages'

    def logic_delete(self):
        self.state = Message.MessageState.DELETED
        self.save()

    def __str__(self):
        return self.text
    

    class Meta:
        db_table = 'messages'