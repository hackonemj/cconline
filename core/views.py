import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from automovel.models import Automovel
from conta.models import User
from core.filters import ServicoDiarioFilter
from recurso_humano.models import RecursoHumano
from servico.models import Servico
from servico_diario.forms import CondutorServicoDiarioForm
from servico_diario.models import ServicoDiario, CO

from django.core.paginator import Paginator


def inicio(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('conta:entrar')

    else:
        if user.is_staff:
            servico_zona = None
            if 'co' in request.GET:
                temp_sd = request.GET.get('co', False)
                servico_zona = temp_sd

            rh_pendentes = []
            servico_pendentes = []
            automovel_pendentes = []

            template_staff = 'inicio_staff.html'
            template_name = template_staff
            sd_filter = ServicoDiarioFilter(request.GET, queryset=ServicoDiario.objects.filter(validar_servico=False))

            if ServicoDiario.objects.all() and servico_zona:
                if not sd_filter.qs:
                    temp_co = get_object_or_404(CO, id=servico_zona)
                    print(Servico.objects.filter(zona=temp_co.nome))
                    # Servico
                    for s in Servico.objects.filter(zona=temp_co.nome):
                        data = {'zona': s.zona, 'nome': s.nome, 'cliente': s.cliente}
                        servico_pendentes.append(data)

                    # Automovel
                    for auto in Automovel.objects.filter(co=temp_co.nome):
                        data = {'marca': auto.marca, 'matricula': auto.matricula}
                        automovel_pendentes.append(data)

                    # Recursos humanos
                    for rh in RecursoHumano.objects.filter(co=temp_co.nome):
                        data = {'numero_funcionario': rh.id_funcionario, 'nome_completo': rh.nome_completo}
                        rh_pendentes.append(data)

                else:
                    temp_co = get_object_or_404(CO, id=servico_zona)
                    # Servico
                    for s in Servico.objects.filter(zona__iexact=temp_co.nome):
                        data = {'zona': s.zona, 'nome': s.nome, 'cliente': s.cliente}
                        servico_pendentes.append(data)

                    print(servico_pendentes)

                    temp_sd = sd_filter.qs.filter(co=servico_zona)

                    # Automovel
                    for auto in Automovel.objects.filter(co__iexact=temp_co.nome):
                        data = {'marca': auto.marca, 'matricula': auto.matricula}
                        automovel_pendentes.append(data)

                    # Recursos humanos
                    for rh in RecursoHumano.objects.filter(co__iexact=temp_co.nome):
                        data = {'numero_funcionario': rh.id_funcionario, 'nome_completo': rh.nome_completo}
                        rh_pendentes.append(data)

                    for temp_sd in temp_sd:
                        for rh in rh_pendentes:
                            if rh['numero_funcionario'] == temp_sd.condutor.funcionario_id:
                                rh_pendentes.remove(rh)

                        for auto in automovel_pendentes:
                            if auto['matricula'] == temp_sd.automovel.matricula:
                                automovel_pendentes.remove(auto)

                        for s in servico_pendentes:
                            if s['zona'] == temp_sd.servico.zona and s['nome'] == temp_sd.servico.nome:
                                servico_pendentes.remove(s)

            context = {
                "user": user,
                'filter': sd_filter,
                'servico_pendentes': servico_pendentes,
                'automovel_pendentes': automovel_pendentes,
                'rh_pendentes': rh_pendentes,
            }

        else:
            template_condutor = 'inicio_driver.html'
            template_name = template_condutor

            servico_diario = ServicoDiario.objects.filter(condutor__username__iexact=user.username,
                                                          estado_concluido=False)
            has_active_sd = False
            if servico_diario.count() > 0:
                has_active_sd = True

            if request.method == 'POST':
                form = CondutorServicoDiarioForm(request.POST)
                if form.is_valid():
                    novo_sd = form.save(commit=False)
                    novo_sd.condutor = get_object_or_404(User, username=user.username)
                    novo_sd.automovel = get_object_or_404(Automovel,
                                                          matricula=form.cleaned_data['automovel_matricula'].upper())
                    novo_sd.servico = get_object_or_404(Servico, codigo=form.cleaned_data['codigo_do_servico'].upper())

                    if CO.objects.filter(nome=novo_sd.servico.zona).exists():
                        novo_sd.co = CO.objects.get(nome__iexact=novo_sd.servico.zona)
                    else:
                        novo_sd.co = CO.objects.create(nome=novo_sd.servico.zona, slug=novo_sd.servico.zona)

                    novo_sd.estado_concluido = False
                    novo_sd.validar_servico = False
                    novo_sd.supervisor = None
                    novo_sd.km_final = 0
                    form.save()
                    return redirect("core:inicio")

            else:
                form = CondutorServicoDiarioForm()

            context = {
                'user': user,
                'form': form,
                'servico_diario': servico_diario,
                'has_active_SD': has_active_sd,
            }

    return render(request, template_name, context)


def validar_servico_diario(request, sd_id):
    user = request.user
    servicos_diario = ServicoDiario.objects.get(pk=sd_id)
    servicos_diario.validar_servico = True
    servicos_diario.supervisor = get_object_or_404(User, username=user.username)
    servicos_diario.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def validar_servico_completed(request):
    # Todo.objects.filter(complete__exact=True).delete()
    servicos_diarios = ServicoDiario.objects.filter(validar_servico__exact=False)
    return redirect('core:inicio')


def validate_codigo_servico(request):
    codigo_do_servico = request.GET.get('codigo_do_servico', None)

    if Servico.objects.filter(codigo__iexact=codigo_do_servico.upper()).exists():
        servico = Servico.objects.get(codigo__iexact=codigo_do_servico.upper())
        data = {
            'encontrou': True,
            'cliente': servico.cliente,
            'nome': servico.nome,
        }
    else:
        data = {
            'encontrou': False,
        }

    return JsonResponse(data)


def validate_automovel_matricula(request):
    automovel_matricula = request.GET.get('automovel_matricula', None)
    if Automovel.objects.filter(matricula__iexact=automovel_matricula.upper()).exists():
        automovel = get_object_or_404(Automovel, matricula=automovel_matricula.upper())
        if automovel.km_actual == 0 or automovel.km_actual is None:
            km = 0

        else:
            km = automovel.km_actual

        data = {
            'encontrou': True,
            'automovel_modelo': automovel.modelo,
            'automovel_km_actual': km
        }

    else:
        data = {
            'encontrou': False,
        }
    return JsonResponse(data)


def ajax_finalizar_servico(request, id):
    temp_km_final = request.POST.get('km_final', False)
    km_final = 0
    if temp_km_final is not None and temp_km_final.isnumeric():
        km_final = int(temp_km_final)

    data = {'concluido': False, }
    if request.is_ajax():

        if ServicoDiario.objects.filter(id__iexact=id).exists():
            servico_diario = get_object_or_404(ServicoDiario, id=id)

            if km_final > servico_diario.km_inicial:
                servico_diario.estado_concluido = True
                servico_diario.finished_at = datetime.datetime.now()
                servico_diario.km_final = km_final
                servico_diario.automovel.km_actual = km_final
                Automovel.objects.filter(matricula__iexact=servico_diario.automovel.matricula).update(
                    km_actual=km_final)
                servico_diario.save()
                data = {
                    'concluido': True,
                }

            else:
                raise Exception('A kilometragem final não pode ser inferior a kilometragem inicial')

        return JsonResponse(data)
    else:
        raise Http404


@login_required
def minhas_viagens(request):
    user = request.user
    template_name = 'minhas_viagens.html'

    servicos_diarios_list = ServicoDiario.objects.filter(condutor__username__iexact=user.username,
                                                         estado_concluido=True).order_by('-finished_at')

    paginator = Paginator(servicos_diarios_list, 9)  # Show 25 contacts per page

    page = request.GET.get('page')
    servicos_diarios = paginator.get_page(page)

    context = {
        'servicos_diarios': servicos_diarios,
    }
    return render(request, template_name, context)
