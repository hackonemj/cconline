# Generated by Django 2.1.1 on 2018-09-18 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servico_diario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicodiario',
            name='finished_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Concluído em'),
        ),
    ]