# Generated by Django 3.0.5 on 2020-04-28 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dreams', '0005_auto_20200426_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dream',
            name='type',
            field=models.CharField(choices=[('sleep', 'Sleep'), ('daydream', 'Daydream'), ('psychedelic', 'Psychedelic'), ('other', 'Other')], default='sleep', max_length=25, verbose_name='dream type'),
        ),
    ]
