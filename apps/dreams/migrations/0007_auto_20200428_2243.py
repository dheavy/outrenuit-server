# Generated by Django 3.0.5 on 2020-04-28 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dreams', '0006_auto_20200428_2202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dream',
            name='user',
        ),
        migrations.AddField(
            model_name='dream',
            name='dreamer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dreamer', to=settings.AUTH_USER_MODEL, verbose_name='dreamer'),
        ),
    ]
