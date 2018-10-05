from django.db.models import Q
from model_utils import Choices
from django.db import models

ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'dono'),
    ('2', 'matricula'),
    ('3', 'marca'),
    ('4', 'modelo'),
    ('5', 'data_matricula'),
    ('6', 'co'),
    ('7', 'fim_prestacao'),
    ('8', 'prestacao'),
    ('9', 'validade'),
)


class Automovel(models.Model):
    activo = models.CharField('Activo', max_length=2)
    dono = models.CharField('Dono', max_length=30)
    matricula = models.CharField('Matricula', max_length=20)
    marca = models.CharField('Marca', max_length=30)
    modelo = models.CharField('Modelo', max_length=80)
    data_matricula = models.DateField('Data matricula', blank=True, null=True)
    co = models.CharField('CO', max_length=30)
    inpencao = models.DateField('Inspenção', blank=True, null=True)
    licenca_alvara = models.DateField('Licença alvara', blank=True, null=True)
    cartrack = models.CharField('Cartrack', max_length=10, blank=True, null=True)
    km_actual = models.BigIntegerField('Kilometros actual', blank=True, null=True)
    cv = models.PositiveIntegerField('CV', blank=True, null=True)
    combustivel = models.CharField('Combustivel', max_length=40)
    peso_bruto = models.DecimalField('Peso bruto', decimal_places=2, max_digits=12, blank=True, null=True)
    cc = models.DecimalField('CC', decimal_places=2, max_digits=12, blank=True, null=True)
    iuc = models.PositiveIntegerField('IUC', blank=True, null=True)
    valor_actual_do_veiculo = models.DecimalField('Valor actual do veiculo', decimal_places=3, max_digits=12,
                                                  blank=True, null=True)
    prestacao = models.DecimalField('Prestação', decimal_places=2, max_digits=12, blank=True, null=True)
    manut_km = models.DecimalField('Manut km', decimal_places=2, max_digits=12)
    valor_dia = models.DecimalField('Valor dia', decimal_places=2, max_digits=12)
    lt100 = models.PositiveIntegerField('Lt 100')
    fim_prestacao = models.DateField('Fim prestação', blank=True, null=True)
    contrato = models.CharField('Contrato', max_length=60, blank=True, null=True)
    financeira = models.CharField('Financeira', max_length=60, blank=True, null=True)
    obs = models.PositiveIntegerField('Observação', blank=True, null=True)
    banco_de_pagamento = models.CharField('Banco de pagamento', max_length=60, blank=True, null=True)
    dia_prestacao = models.PositiveIntegerField('Dia de prestação', blank=True, null=True)
    seguro = models.CharField('Seguro', max_length=80, blank=True, null=True)
    valor_do_seguro_anual = models.DecimalField('Valor anual do seguro anual', decimal_places=2, max_digits=12,
                                                blank=True, null=True)
    validade = models.DateField('Validade', blank=True, null=True)

    def __str__(self):
        return self.matricula

    # META CLASS
    class Meta:
        db_table = "automovel"
        verbose_name = 'automovel'
        verbose_name_plural = 'Automoveis'


def query_automoveis_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES[order_column]
    # django orm '-' -> desc
    if order == 'desc':
        order_column = '-' + order_column

    queryset = Automovel.objects.all()
    total = queryset.count()

    ('0', 'id'),
    ('1', 'dono'),
    ('2', 'matricula'),
    ('3', 'marca'),
    ('4', 'modelo'),
    ('5', 'data_matricula'),
    ('6', 'co'),
    ('7', 'fim_prestacao'),
    ('8', 'prestacao'),
    ('9', 'validade'),

    if search_value:
        queryset = queryset.filter(
            Q(id__icontains=search_value) |
            Q(dono__icontains=search_value) |
            Q(matricula__icontains=search_value) |
            Q(marca__icontains=search_value) |
            Q(modelo__icontains=search_value) |
            Q(data_matricula__icontains=search_value) |
            Q(co__icontains=search_value) |
            Q(fim_prestacao__icontains=search_value) |
            Q(prestacao__icontains=search_value) |
            Q(validade__icontains=search_value)
        )

    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length]
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }
