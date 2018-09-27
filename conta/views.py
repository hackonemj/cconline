from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import UserCreationForm, UserLoginForm

@login_required
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


@login_required
def sair(request):
    logout(request)
    return redirect("conta:entrar")
