from import_export import resources
from .models import Servico


class ServicoResource(resources.ModelResource):
    class Meta:
        model = Servico
