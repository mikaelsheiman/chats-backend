# Generated by Django 4.2.4 on 2023-11-20 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_remove_message_replyed_message_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
