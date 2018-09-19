from import_export import resources
from .models import RecursoHumano


class RecursoHumanoResource(resources.ModelResource):
    class Meta:
        model = RecursoHumano
