# Generated by Django 3.2.13 on 2022-05-13 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_logindetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logindetails',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
