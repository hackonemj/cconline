# Generated by Django 2.1.1 on 2018-09-18 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servico_diario', '0003_auto_20180918_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicodiario',
            name='automovel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Automovel', to='automovel.Automovel'),
        ),
    ]