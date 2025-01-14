# Generated by Django 5.0.7 on 2024-10-02 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_customuser_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('song_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=2000)),
                ('singer', models.CharField(max_length=2000)),
                ('tags', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images')),
                ('song', models.FileField(upload_to='images')),
            ],
        ),
    ]
