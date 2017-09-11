# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-15 01:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('code_RH', models.CharField(max_length=10, unique=True, verbose_name=' Code RH')),
                ('nom', models.CharField(max_length=80, verbose_name='Nom et Prénom')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Employée',
            },
        ),
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('lot', models.CharField(max_length=20, verbose_name='Lot')),
                ('peremption', models.DateField(verbose_name='Date de péremption')),
                ('ppa', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='PPA')),
                ('colisage', models.SmallIntegerField(verbose_name='Colisage')),
                ('qtt', models.PositiveIntegerField(verbose_name='Quantité totale du lot')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('hightchart', models.CharField(max_length=15, verbose_name='hightchart produit')),
                ('produit', models.CharField(max_length=150, verbose_name='Désignation du produit')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('table_number', models.IntegerField(verbose_name='numéro de table')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reponsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labeling.Employee', verbose_name='Responsable de la table')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='lot',
            name='produit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labeling.Produit', verbose_name='Produit'),
        ),
    ]