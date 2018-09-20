import datetime

from django.contrib import messages
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

from automovel.models import Automovel
from conta.models import User
from servico.models import Servico
from servico_diario.forms import CondutorServicoDiarioForm
from servico_diario.models import ServicoDiario


def inicio(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('conta:entrar')

    else:
        if user.is_staff:
            template_staff = 'inicio_staff.html'
            template_name = template_staff
            context = {
                "user": user,
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
                    novo_sd.automovel = get_object_or_404(Automovel, matricula=form.cleaned_data['automovel_matricula'].upper())
                    novo_sd.servico = get_object_or_404(Servico, codigo=form.cleaned_data['codigo_do_servico'].upper())
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
    km_final = request.GET.get('km_final', None)

    if request.is_ajax():
        if Servico.objects.filter(id__iexact=id).exists():
            servico_diario = get_object_or_404(ServicoDiario, id=id)

            if int(km_final) > servico_diario.km_inicial:
                servico_diario.estado_concluido = True
                servico_diario.finished_at = datetime.datetime.now()
                servico_diario.km_final = km_final
                servico_diario.automovel.km_actual = km_final
                Automovel.objects.filter(id__iexact=servico_diario.automovel.id).update(km_actual=km_final)
                servico_diario.save()
                data = {
                    'concluido': True,
                }

            else:
                raise Exception('A kilometragem final não pode ser inferior a kilometragem inicial')

        return JsonResponse(data)
    else:
        raise Http404


def minhas_viagens(request):
    user = request.user
    template_name = 'minhas_viagens.html'

    servicos_diarios = ServicoDiario.objects.filter(condutor__username__iexact=user.username,
                                                    estado_concluido=True)
    context = {
        'servicos_diarios': servicos_diarios,
    }

    return render(request, template_name, context)
