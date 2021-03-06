# Generated by Django 2.1.1 on 2018-10-03 10:22

from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Automovel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.CharField(max_length=2, verbose_name='Activo')),
                ('dono', models.CharField(max_length=30, verbose_name='Dono')),
                ('matricula', models.CharField(max_length=20, verbose_name='Matricula')),
                ('marca', models.CharField(max_length=30, verbose_name='Marca')),
                ('modelo', models.CharField(max_length=80, verbose_name='Modelo')),
                ('data_matricula', models.DateField(blank=True, null=True, verbose_name='Data matricula')),
                ('co', models.CharField(max_length=30, verbose_name='CO')),
                ('inpencao', models.DateField(blank=True, null=True, verbose_name='Inspenção')),
                ('licenca_alvara', models.DateField(blank=True, null=True, verbose_name='Licença alvara')),
                ('cartrack', models.CharField(blank=True, max_length=10, null=True, verbose_name='Cartrack')),
                ('km_actual', models.BigIntegerField(blank=True, null=True, verbose_name='Kilometros actual')),
                ('cv', models.PositiveIntegerField(blank=True, null=True, verbose_name='CV')),
                ('combustivel', models.CharField(max_length=40, verbose_name='Combustivel')),
                ('peso_bruto', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Peso bruto')),
                ('cc', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='CC')),
                ('iuc', models.PositiveIntegerField(blank=True, null=True, verbose_name='IUC')),
                ('valor_actual_do_veiculo', models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True, verbose_name='Valor actual do veiculo')),
                ('prestacao', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Prestação')),
                ('manut_km', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Manut km')),
                ('valor_dia', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Valor dia')),
                ('lt100', models.PositiveIntegerField(verbose_name='Lt 100')),
                ('fim_prestacao', models.DateField(blank=True, null=True, verbose_name='Fim prestação')),
                ('contrato', models.CharField(blank=True, max_length=60, null=True, verbose_name='Contrato')),
                ('financeira', models.CharField(blank=True, max_length=60, null=True, verbose_name='Financeira')),
                ('obs', models.PositiveIntegerField(blank=True, null=True, verbose_name='Observação')),
                ('banco_de_pagamento', models.CharField(blank=True, max_length=60, null=True, verbose_name='Banco de pagamento')),
                ('dia_prestacao', models.PositiveIntegerField(blank=True, null=True, verbose_name='Dia de prestação')),
                ('seguro', models.CharField(blank=True, max_length=80, null=True, verbose_name='Seguro')),
                ('valor_do_seguro_anual', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Valor anual do seguro anual')),
                ('validade', models.DateField(blank=True, null=True, verbose_name='Validade')),
            ],
            options={
                'verbose_name': 'automovel',
                'verbose_name_plural': 'Automoveis',
            },
        ),
    ]
