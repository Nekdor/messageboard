# Generated by Django 4.1.2 on 2022-10-24 20:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0007_reply_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reply',
            name='denied',
        ),
        migrations.AddField(
            model_name='reply',
            name='post_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
