# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labeling', '0007_auto_20170725_1200'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='labeling',
            options={'permissions': (('can_add_labeling', 'Ajouter des bons de vignettage'), ('can_view_history', "Voir l'historique"), ('can_view_statistics', 'Voir les statistiques')), 'verbose_name': 'Rapport de vignettage'},
        ),
        migrations.AddField(
            model_name='employee',
            name='actif',
            field=models.BooleanField(default=True, verbose_name='Actif ?'),
        ),
    ]
