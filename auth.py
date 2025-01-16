from functools import wraps
from django.shortcuts import redirect


def login_required(redirect_url='login'):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(redirect_url)
            else:
                return func(request, *args, **kwargs)
        return wrapper
    return decorator

def is_staff_required(redirect_url='login'):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_staff:
                return func(request, *args, **kwargs)
            else:
                return redirect(redirect_url)
        return wrapper
    return decorator