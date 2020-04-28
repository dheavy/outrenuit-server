# Generated by Django 3.0.5 on 2020-04-28 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dreams', '0007_auto_20200428_2243'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('interpretations', '0002_auto_20200426_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='interpretation',
            name='interpreter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interpreter', to=settings.AUTH_USER_MODEL, verbose_name='interpreter'),
        ),
        migrations.AlterField(
            model_name='interpretation',
            name='dream',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interpretations', to='dreams.Dream', verbose_name='dream'),
        ),
    ]
