# Generated by Django 5.0.7 on 2024-10-02 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_article_author_articleseries_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articleseries',
            name='author',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='ArticleSeries',
        ),
    ]