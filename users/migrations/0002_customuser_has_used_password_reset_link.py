# Generated by Django 5.0.7 on 2024-07-29 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='has_used_password_reset_link',
            field=models.BooleanField(default=False),
        ),
    ]