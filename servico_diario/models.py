from django.db import models

from automovel.models import Automovel
from conta.models import User
from servico.models import Servico


class ServicoDiario(models.Model):
    automovel = models.ForeignKey(Automovel, on_delete=models.CASCADE, related_name='Automovel')
    condutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='condutor')
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='Servico')
    km_inicial = models.BigIntegerField('Kilometros iniciais')
    km_final = models.BigIntegerField('Kilometros finais', blank=True, null=True)
    obs = models.TextField('Observção', blank=True, null=True)
    estado_concluido = models.BooleanField('Serviço concluído')
    validar_servico = models.BooleanField('Validar servico')
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supervisor', blank=True, null=True)
    created_at = models.DateField('Criado em', auto_now_add=True)
    finished_at = models.DateTimeField('Concluído em', blank=True, null=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.condutor.first_name

    # META CLASS
    class Meta:
        verbose_name = 'servico diario'
        verbose_name_plural = 'servicos diarios'
