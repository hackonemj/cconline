# Generated by Django 2.1.1 on 2018-09-21 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automovel', '0002_auto_20180921_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automovel',
            name='banco_de_pagamento',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Banco de pagamento'),
        ),
        migrations.AlterField(
            model_name='automovel',
            name='co',
            field=models.CharField(max_length=30, verbose_name='CO'),
        ),
        migrations.AlterField(
            model_name='automovel',
            name='combustivel',
            field=models.CharField(max_length=30, verbose_name='Combustivel'),
        ),
        migrations.AlterField(
            model_name='automovel',
            name='financeira',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Financeira'),
        ),
        migrations.AlterField(
            model_name='automovel',
            name='marca',
            field=models.CharField(max_length=30, verbose_name='Marca'),
        ),
        migrations.AlterField(
            model_name='automovel',
            name='modelo',
            field=models.CharField(max_length=30, verbose_name='Modelo'),
        ),
    ]