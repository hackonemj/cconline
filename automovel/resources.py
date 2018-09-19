from import_export import resources
from .models import Automovel


class AutomovelResource(resources.ModelResource):
    class Meta:
        model = Automovel
