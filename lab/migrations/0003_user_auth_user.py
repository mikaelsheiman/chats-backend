# Generated by Django 4.2.6 on 2023-11-13 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0002_chat_messagestate_user_message_chatuser_chat_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auth_user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='lab.authuser'),
            preserve_default=False,
        ),
    ]
