# Generated by Django 2.1.1 on 2018-09-18 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.CharField(max_length=2, verbose_name='Activo')),
                ('codigo', models.CharField(max_length=10, unique=True, verbose_name='Código')),
                ('zona', models.CharField(max_length=5, verbose_name='Zona')),
                ('cliente', models.CharField(max_length=20, verbose_name='Cliente')),
                ('nome', models.CharField(max_length=35, verbose_name='Nome')),
                ('valor_dia', models.PositiveIntegerField(null=True, verbose_name='Valor dia')),
                ('portagens', models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='Postagens')),
                ('fatura', models.CharField(max_length=30, null=True, verbose_name='Fatura')),
            ],
        ),
    ]
