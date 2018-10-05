from rest_framework import serializers

from .models import Servico


class ServicoSerializer(serializers.ModelSerializer):
    # If your <field_name> is declared on your serializer with the parameter required=False
    # then this validation step will not take place if the field is not included.

    class Meta:
        model = Servico
        # fields = '__all__'
        fields = ('id', 'activo', 'codigo', 'zona', 'cliente', 'nome', 'valor_dia', 'portagens', 'banca', 'fatura')
