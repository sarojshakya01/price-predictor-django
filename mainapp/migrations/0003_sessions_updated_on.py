# Generated by Django 3.0.7 on 2020-07-11 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_sessions'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessions',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]