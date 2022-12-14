# Generated by Django 4.1.1 on 2022-10-09 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='course',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='staff',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='course',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='leavereportstaff',
            name='date',
            field=models.DateField(max_length=60),
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
    ]
