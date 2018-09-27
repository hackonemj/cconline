from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from servico.models import Servico

@login_required
def servico(request):
    servico_list = Servico.objects.all().order_by('zona')

    paginator = Paginator(servico_list, 25)  # Show 25 servicos per page

    page = request.GET.get('page')
    servicos = paginator.get_page(page)

    context = {
        'servicos': servicos,
    }
    return render(request, 'servico.html', context)