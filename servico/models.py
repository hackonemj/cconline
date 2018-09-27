from django.db import models


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
        ordering = ['zona', ]
