from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from conta.models import User
from core.decorators import logged_in_required, user_admin_required
from recurso_humano.models import RecursoHumano
from .forms import UserCreationForm, UserLoginForm


@user_admin_required
def criar_conta(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("conta:entrar")
    context = {
        'form': form
    }
    return render(request, "signup.html", context)


def entrar(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect("core:inicio")

    else:
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            user_obj = form.cleaned_data.get('user_obj')
            login(request, user_obj)
            return redirect("core:inicio")

    return render(request, "login.html", {"form": form})


@logged_in_required
def sair(request):
    logout(request)
    return redirect("conta:entrar")


@logged_in_required
def ver_perfil(request):
    user = User.objects.get(username__iexact=request.user.username)
    template_name = 'perfil.html'

    if RecursoHumano.objects.filter(id_funcionario__exact=user.funcionario_id).exists():
        rh = RecursoHumano.objects.get(id_funcionario__exact=user.funcionario_id)

    else:
        rh = None

    context = {
        'user': user,
        'rh_data': rh,
    }
    return render(request, template_name, context)
