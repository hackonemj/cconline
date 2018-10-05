from django.http import HttpResponse
from django.template.response import TemplateResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from automovel.models import Automovel, query_automoveis_by_args
from automovel.serializers import AutomovelSerializer
from core.decorators import user_supervisor_or_admin_required


@user_supervisor_or_admin_required
def automovel_with_jquery(request):
    html = TemplateResponse(request, 'automovel.html')
    return HttpResponse(html.render())


class AutomovelViewSet(viewsets.ModelViewSet):
    queryset = Automovel.objects.all()
    serializer_class = AutomovelSerializer

    def list(self, request, **kwargs):
        try:
            automovel = query_automoveis_by_args(**request.query_params)
            serializer = AutomovelSerializer(automovel['items'], many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = automovel['draw']
            result['recordsTotal'] = automovel['total']
            result['recordsFiltered'] = automovel['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)
