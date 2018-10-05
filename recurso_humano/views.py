from django.contrib.auth.decorators import login_required

from core.decorators import user_supervisor_or_admin_required
from .models import RecursoHumano
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

@user_supervisor_or_admin_required
def recurso_humano(request):
    recurso_humano_list = RecursoHumano.objects.all().order_by('co')
    n_total_funcionarios = RecursoHumano.objects.all().count()
    total_funcionarios_activos = RecursoHumano.objects.filter(activo='S').count()
    total_funcionarios_nao_activos = RecursoHumano.objects.filter(activo='N').count()

    paginator = Paginator(recurso_humano_list, 25)  # Show 25 rh per page

    page = request.GET.get('page')
    recurso_humanos = paginator.get_page(page)

    context = {
        'recurso_humanos': recurso_humanos, 'funcionarios': n_total_funcionarios,
        'total_func_activos': total_funcionarios_activos,
        'total_func_nao_activos': total_funcionarios_nao_activos,
    }
    return render(request, 'rh.html', context)
