# Generated by Django 3.1.5 on 2021-02-01 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0010_auto_20210201_1427'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='subject',
            new_name='sender',
        ),
        migrations.AddField(
            model_name='message',
            name='sebject',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
