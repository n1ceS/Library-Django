# Generated by Django 3.1.5 on 2021-01-29 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0005_book_publisher'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]