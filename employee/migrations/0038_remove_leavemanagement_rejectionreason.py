# Generated by Django 3.2.13 on 2022-06-06 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0037_auto_20220606_1803'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leavemanagement',
            name='rejectionreason',
        ),
    ]