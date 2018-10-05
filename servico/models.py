from django.db.models import Q
from model_utils import Choices
from django.db import models

ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'activo'),
    ('2', 'codigo'),
    ('3', 'zona'),
    ('4', 'cliente'),
    ('5', 'nome'),
    ('6', 'valor_dia'),
    ('7', 'portagens'),
    ('8', 'banca'),
    ('9', 'fatura'),
)


class Servico(models.Model):
    activo = models.CharField('Activo', max_length=2)
    codigo = models.CharField('Código', max_length=10, unique=True)
    zona = models.CharField('Zona', max_length=10)
    cliente = models.CharField('Cliente', max_length=20)
    nome = models.CharField('Nome', max_length=50)
    valor_dia = models.PositiveIntegerField('Valor dia', null=True)
    portagens = models.DecimalField('Postagens', decimal_places=2, max_digits=12, null=True)
    banca = models.PositiveIntegerField('Banca', null=True)
    fatura = models.CharField('Fatura', max_length=30, null=True)

    def __str__(self):
        return '{} - {}'.format(self.zona, self.nome)

    class Meta:
        db_table = "servico"
        ordering = ['zona', ]


def query_servicos_by_args(**kwargs):
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

    queryset = Servico.objects.all()
    total = queryset.count()

    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(activo__icontains=search_value) |
                                   Q(codigo__icontains=search_value) |
                                   Q(zona__icontains=search_value) |
                                   Q(cliente__icontains=search_value) |
                                   Q(nome__icontains=search_value) |
                                   Q(valor_dia__icontains=search_value) |
                                   Q(portagens__icontains=search_value) |
                                   Q(banca__icontains=search_value) |
                                   Q(fatura__icontains=search_value)
                                   )

    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length]
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }
