# Generated by Django 5.0.7 on 2024-07-30 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_customuser_has_used_password_reset_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='description',
        ),
    ]