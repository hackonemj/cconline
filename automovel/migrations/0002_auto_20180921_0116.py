# Generated by Django 2.1.1 on 2018-09-21 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automovel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automovel',
            name='dono',
            field=models.CharField(max_length=30, verbose_name='Dono'),
        ),
    ]