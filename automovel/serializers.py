from rest_framework import serializers

from .models import Automovel


class AutomovelSerializer(serializers.ModelSerializer):
    # If your <field_name> is declared on your serializer with the parameter required=False
    # then this validation step will not take place if the field is not included.

    class Meta:
        model = Automovel
        # fields = '__all__'
        fields = (
            'id', 'dono', 'matricula', 'marca', 'modelo', 'data_matricula', 'co', 'fim_prestacao', 'prestacao',
            'validade'
        )