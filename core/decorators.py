from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def logged_in_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return redirect('conta:entrar')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_supervisor_or_admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_supervisor:
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
