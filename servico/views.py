from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from core.decorators import user_supervisor_or_admin_required
from servico.models import Servico, query_servicos_by_args
from servico.serializers import ServicoSerializer


@user_supervisor_or_admin_required
def servico(request):
    servico_list = Servico.objects.all().order_by('zona')

    paginator = Paginator(servico_list, 25)  # Show 25 servicos per page

    page = request.GET.get('page')
    servicos = paginator.get_page(page)

    context = {
        'servicos': servicos,
    }
    return render(request, 'servico.html', context)


@user_supervisor_or_admin_required
def index(request):
    html = TemplateResponse(request, 'index.html')
    return HttpResponse(html.render())


class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer

    def list(self, request, **kwargs):
        try:
            music = query_servicos_by_args(**request.query_params)
            serializer = ServicoSerializer(music['items'], many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = music['draw']
            result['recordsTotal'] = music['total']
            result['recordsFiltered'] = music['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)
