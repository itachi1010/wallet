# Generated by Django 4.2.7 on 2023-12-01 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profile_date_of_birth_profile_full_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='is_wallet_change',
        ),
    ]
