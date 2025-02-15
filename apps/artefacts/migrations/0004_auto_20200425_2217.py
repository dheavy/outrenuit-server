# Generated by Django 3.0.5 on 2020-04-25 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artefacts', '0003_auto_20200425_1919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artefact',
            name='span',
        ),
        migrations.AddField(
            model_name='artefact',
            name='label_end',
            field=models.IntegerField(default=0, help_text='End position in original string'),
        ),
        migrations.AddField(
            model_name='artefact',
            name='label_start',
            field=models.IntegerField(default=0, help_text='Start position in original string'),
        ),
    ]
