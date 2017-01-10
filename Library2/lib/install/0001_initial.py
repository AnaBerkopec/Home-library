# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-17 13:04
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
            name='Izposojeno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('izposoja', models.DateTimeField()),
                ('vracilo', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Knjiga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avtorji', models.CharField(max_length=200)),
                ('naslov', models.CharField(max_length=200)),
                ('dodajalec', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lokacija',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nadstropje', models.IntegerField(max_length=3)),
                ('omara', models.IntegerField(max_length=3)),
                ('polica', models.IntegerField(max_length=3)),
            ],
        ),
        migrations.AddField(
            model_name='knjiga',
            name='lokacija',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lib.Lokacija'),
        ),
        migrations.AddField(
            model_name='izposojeno',
            name='knjiga',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lib.Knjiga'),
        ),
        migrations.AddField(
            model_name='izposojeno',
            name='uporabnik',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]