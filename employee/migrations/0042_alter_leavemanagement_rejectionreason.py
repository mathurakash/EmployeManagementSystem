# Generated by Django 3.2.13 on 2022-06-06 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0041_alter_leavemanagement_rejectionreason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavemanagement',
            name='rejectionreason',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
