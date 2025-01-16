from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm
from django import forms

from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncDate

import logging, auth
logger = logging.getLogger('django')


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('products')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('products')
    else:
        form = LoginForm()
    data = {
        'form': form,
        'page_name': "ACRM Вход"
    }
    return render(request, 'user/login.html', data)

@auth.is_staff_required(redirect_url='profile')
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            if user is not None:
                return redirect('profile')
    else:
        form = RegisterForm()
    data = {
        'form': form,
        'page_name': "ACRM Регистрация"
    }
    return render(request, 'user/register.html', data)

@auth.is_staff_required(redirect_url='profile')
def upd_user(request, uID):
    if not uID: return Http404
    user = get_object_or_404(User, id=uID)

    if request.method == "GET":
        data = {
            'page_name': 'Редактировать продукт',
            'name': "update",
            'form': RegisterForm(instance=user),
        }
        return render(request, "product/forms/my_products.htm", data)
    elif request.method == "POST":
        form = RegisterForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect('profile')
        return JsonResponse({'message': form.errors}, status=400)
    else:
        return Http404

def sign_out(request):
    logout(request)
    return redirect('login')


@auth.login_required(redirect_url='login')
def profile(request):
    users = User.objects.all()

    context = {
        'page_name': f"Профиль - {request.user.username}",
        'users': users if request.user.is_staff else None
    }
    return render(request, 'user/profile.html', context)