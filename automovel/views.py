from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from automovel.models import Automovel

@login_required
def automovel(request):
    automovel_list = Automovel.objects.all().order_by('dono')

    paginator = Paginator(automovel_list, 25)  # Show 25 automovel per page

    page = request.GET.get('page')
    automoveis = paginator.get_page(page)

    context = {
        'automoveis': automoveis,
    }
    return render(request, 'automovel.html', context)