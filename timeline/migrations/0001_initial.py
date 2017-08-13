# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-12 16:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('perfis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Postagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteudo', models.CharField(blank=True, max_length=256)),
                ('imagem', models.ImageField(null=True, upload_to='postagens/')),
                ('data_criacao', models.DateTimeField()),
                ('data_edicao', models.DateTimeField(null=True)),
                ('visibilidade', models.BooleanField(default=True)),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postagens', to='perfis.Perfil')),
            ],
        ),
    ]
