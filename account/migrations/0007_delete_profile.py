# Generated by Django 4.2.11 on 2024-05-20 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_customuser_username'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]