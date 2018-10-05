from django import forms

from automovel.models import Automovel
from servico.models import Servico
from .models import ServicoDiario


class CondutorServicoDiarioForm(forms.ModelForm):
    automovel_matricula = forms.CharField(label='Automovel matricula', )
    automovel_modelo = forms.CharField(label='Modelo', )
    codigo_do_servico = forms.CharField(label='Código do serviço', )
    descricao_servico = forms.CharField(label='Descrição serviço', )

    class Meta:
        model = ServicoDiario
        exclude = ['automovel', 'supervisor', 'km_final', 'estado_concluido', 'validar_servico', 'condutor',
                   'finished_at']
        fields = ['automovel_matricula', 'automovel_modelo', 'codigo_do_servico', 'descricao_servico', 'km_inicial',
                  'obs']

    def clean(self):
        cleaned_data = super(CondutorServicoDiarioForm, self).clean()
        automovel_matricula = cleaned_data.get('automovel_matricula')
        codigo_do_servico = cleaned_data.get('codigo_do_servico')
        km_inicial = cleaned_data.get('km_inicial')

        if not automovel_matricula and not codigo_do_servico and not km_inicial:
            raise forms.ValidationError('Preeacha todos os campos obrigatórios!')

        else:

            if (Automovel.objects.filter(matricula=automovel_matricula).exists() and Servico.objects.filter(
                    codigo__iexact=codigo_do_servico).exists()) is False:
                raise forms.ValidationError("Matricula ou código do serviço não existe!")