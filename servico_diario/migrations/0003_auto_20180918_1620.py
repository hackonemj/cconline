# Generated by Django 2.1.1 on 2018-09-18 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servico_diario', '0002_auto_20180918_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicodiario',
            name='finished_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Concluído em'),
        ),
        migrations.AlterField(
            model_name='servicodiario',
            name='km_final',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Kilometros finais'),
        ),
    ]
