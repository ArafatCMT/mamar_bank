# Generated by Django 5.0.6 on 2024-06-19 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbankaccount',
            name='is_bankrupt',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]