# Generated by Django 4.2.6 on 2023-11-14 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0004_rename_user_client_alter_client_auth_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatuser',
            old_name='unread_messages',
            new_name='read_messages',
        ),
        migrations.AddField(
            model_name='chat',
            name='messages_total',
            field=models.BigIntegerField(blank=True, default=0),
        ),
    ]
