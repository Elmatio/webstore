# Generated by Django 4.2.11 on 2024-04-29 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_cart_session_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='session',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
