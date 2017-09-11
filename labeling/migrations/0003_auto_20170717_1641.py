# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 16:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('labeling', '0002_labeling_labelingdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabelingDetailsTempo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('labeling_qtt', models.PositiveSmallIntegerField(verbose_name='Nombre de vignette collées')),
                ('souches_qtt', models.PositiveSmallIntegerField(verbose_name='Nombre de souches collés')),
                ('unlabeling_qtt', models.PositiveSmallIntegerField(verbose_name='Nombre de vignette enlevées')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labeling.Employee', verbose_name='vignetteur')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='labeling',
            options={'verbose_name': 'Rapport de vignettage'},
        ),
        migrations.AlterModelOptions(
            name='labelingdetails',
            options={'verbose_name': 'Détails du rapport de vignettage'},
        ),
    ]