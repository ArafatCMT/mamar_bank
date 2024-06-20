# Generated by Django 5.0.6 on 2024-06-20 04:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_userbankaccount_bankrupt_delete_bankrupt'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankRupt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bankrupt', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='userbankaccount',
            name='bankrupt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.bankrupt'),
        ),
    ]