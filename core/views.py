import datetime

from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from automovel.models import Automovel
from conta.models import User
from core.decorators import logged_in_required
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


@logged_in_required
def validar_servico_diario(request, sd_id):
    user = request.user
    servicos_diario = ServicoDiario.objects.get(pk=sd_id)
    servicos_diario.validar_servico = True
    servicos_diario.supervisor = get_object_or_404(User, username=user.username)
    servicos_diario.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@logged_in_required
def validar_servico_completed(request):
    servicos_diarios = ServicoDiario.objects.filter(validar_servico__exact=False)
    return redirect('core:inicio')


@logged_in_required
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


@logged_in_required
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


@logged_in_required
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


@logged_in_required
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


# validar funcionário
@logged_in_required
def validate_funcionario(request):
    id_funcionario = request.GET.get('id_funcionario', None)

    if RecursoHumano.objects.filter(id_funcionario__exact=id_funcionario).exists() and User.objects.filter(
            funcionario_id__exact=id_funcionario).exists():

        funcionario = User.objects.get(funcionario_id__exact=id_funcionario)
        data = {
            'encontrou': True,
            'nome': funcionario.get_full_name(),
        }
    else:
        data = {
            'encontrou': False,
        }

    return JsonResponse(data)


def ajax_criar_sd(request):
    id_funcionario = request.POST.get('id_funcionario', None)
    codigo_servico = request.POST.get('codigo_servico', None)
    auto_matricula = request.POST.get('auto_matricula', None)
    km_inicial = request.POST.get('km_inicial', None)
    km_final = request.POST.get('km_final', None)
    obs = request.POST.get('obs', None)

    # print("{} {} {} {} {} {}".format(temp_id, codigo_servico, auto_matricula, km_final, km_inicial, obs))

    data = {'concluido': False, }

    if request.method == "POST" and request.is_ajax:
        condutor = User.objects.get(funcionario_id__exact=id_funcionario)
        automovel = Automovel.objects.get(matricula__iexact=auto_matricula)
        servico = Servico.objects.get(codigo__iexact=codigo_servico)

        novo_sd = ServicoDiario(automovel=automovel, condutor=condutor, servico=servico, km_inicial=km_inicial,
                                km_final=km_final)

        if CO.objects.filter(nome=novo_sd.servico.zona).exists():
            novo_sd.co = CO.objects.get(nome__iexact=novo_sd.servico.zona)
        else:
            novo_sd.co = CO.objects.create(nome=novo_sd.servico.zona, slug=novo_sd.servico.zona)

        novo_sd.automovel.km_actual = novo_sd.km_final
        Automovel.objects.filter(matricula__iexact=novo_sd.automovel.matricula).update(km_actual=km_final)
        novo_sd.estado_concluido = True
        novo_sd.finished_at = datetime.datetime.now()
        novo_sd.validar_servico = False
        novo_sd.supervisor = None
        novo_sd.obs = obs
        novo_sd.save()

        return JsonResponse(data)
    else:
        raise Http404
