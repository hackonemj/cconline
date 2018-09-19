from django.db import models


class RecursoHumano(models.Model):
    activo = models.CharField('Activo', max_length=2)
    nif = models.PositiveIntegerField('NIF', null=True)
    co = models.CharField('CO', max_length=20)
    id_funcionario = models.IntegerField('Nº', default=0)
    nome_completo = models.CharField('Nome completo', max_length=35)
    nome = models.CharField('Nome', max_length=30, null=True)
    obs = models.CharField('OBS', max_length=30)

    def __str__(self):
        return self.nome_completo