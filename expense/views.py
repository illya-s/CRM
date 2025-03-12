from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse, Http404
from django.forms.models import model_to_dict
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import *
from .forms import *
# from .tasks import *

import datetime
from datetime import timedelta
from django.utils import timezone

import requests, auth
from config import np_url, api_key


@auth.login_required(redirect_url='login')
def expenses(request):
    ECatList = ExpenseCategory.objects.all()
    context = {
        'eCatList': ECatList
    }
    return render(request, 'expense/expenses.htm', context)

@auth.login_required(redirect_url='login')
def cat_list(request):
    ECatList = ExpenseCategory.objects.all()
    context = {'eCatList': ECatList}
    return JsonResponse({'list': render_to_string('expense/cat_list.htm', context),})

@auth.is_staff_required(redirect_url='expenses')
def add_expense_cat(request):
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('expenses')
        return JsonResponse({ 'message': form.errors }, status=400)
    else:
        form = ExpenseCategoryForm()
        context = { 'form': form, 'page': "create_expense_category", 'page_name': 'Добавить категорию расходов' }
        return render(request, 'expense/form.htm', context)
@auth.is_staff_required(redirect_url='expenses')
def upd_expense_cat(request, pk):
    expense_cat = get_object_or_404(ExpenseCategory, pk=pk)

    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST, request.FILES, instance=expense_cat)
        if form.is_valid():
            form.save()
            return redirect('expenses')
        return JsonResponse({ 'message': form.errors }, status=400)
    else:
        form = ExpenseCategoryForm(instance=expense_cat)
        context = { 'form': form, 'page': "create_expense_category", 'page_name': 'Редактировать категорию расходов' }
        return render(request, 'expense/form.htm', context)
@auth.is_staff_required(redirect_url='expenses')
def del_expense_cat(request):
    if request.method == 'POST':
        expense_cat = get_object_or_404(ExpenseCategory, pk=request.POST.get('cID'))
        expense_cat.delete()

        return JsonResponse({ 'message': 'sucses' }, status=200)
    else:
        return Http404



@auth.login_required(redirect_url='login')
def plat_list(request):
    EPlatList = ExpensePlatform.objects.all()
    context = {'ePlatList': EPlatList}
    return JsonResponse({'list': render_to_string('expense/plat_list.htm', context),})

@auth.is_staff_required(redirect_url='expenses')
def add_expense_plat(request):
    if request.method == 'POST':
        form = ExpensePlatformForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('expenses')
        return JsonResponse({ 'message': form.errors }, status=400)
    else:
        form = ExpensePlatformForm()
        context = { 'form': form, 'page': "create_expense_category", 'page_name': 'Добавить платформу расходов' }
        return render(request, 'expense/form.htm', context)
@auth.is_staff_required(redirect_url='expenses')
def upd_expense_plat(request, pk):
    expense_cat = get_object_or_404(ExpenseCategory, pk=pk)

    if request.method == 'POST':
        form = ExpensePlatformForm(request.POST, request.FILES, instance=expense_cat)
        if form.is_valid():
            form.save()
            return redirect('expenses')
        return JsonResponse({ 'message': form.errors }, status=400)
    else:
        form = ExpensePlatformForm(instance=expense_cat)
        context = { 'form': form, 'page': "create_expense_category", 'page_name': 'Редактировать платформу расходов' }
        return render(request, 'expense/form.htm', context)
@auth.is_staff_required(redirect_url='expenses')
def del_expense_plat(request):
    if request.method == 'POST':
        expense_cat = get_object_or_404(ExpenseCategory, pk=request.POST.get('cID'))
        expense_cat.delete()

        return JsonResponse({ 'message': 'sucses' }, status=200)
    else:
        return Http404



def expense_list(request):
    now = datetime.datetime.now()

    if request.method != "GET":
        return Http404

    # expense per page
    spp = request.GET.get('epp') if request.GET.get('epp') else 25

    # page number
    page = int(request.GET.get('page')) if request.GET.get('page') else 1

    # filter
    f = request.GET.get('filter')

    ymd = request.GET.get('ymd')

    # year month
    y, m, d = tuple(str(ymd).split(',')) if ymd and ymd != "undefined" else (now.year, "-1", "-1")

    if f != "-1":
        eCat = get_object_or_404(ExpenseCategory, id=f)
        objs = eCat.category_expenses.all()
    else:
        objs = Expense.objects.all()

    objs = objs.filter(date__year=y)

    unique_years  = objs.values('date__year').distinct()
    years_list = [el['date__year'] for el in unique_years]

    unique_months = objs.values('date__month').distinct()
    month_list = [el['date__month'] for el in unique_months]

    if m != '-1':
        objs = objs.filter(date__month=m)

    unique_days   = objs.values('date__day').distinct()
    day_list   = [el['date__day'] for el in unique_days][::-1]

    if d != '-1':
        objs = objs.filter(date__day=d)

    expenses_obj = [
        {
            **model_to_dict(expense),
            'product': {
                'id': expense.product.pk,
                'name': expense.product.name
            } if expense.product else None,
            'category': expense.category.name,
            'platform': expense.platform.name
        }
        for expense in objs.order_by("-date")
    ]
    paginator = Paginator(expenses_obj, spp)

    try:
        expenses = paginator.page(page)
    except PageNotAnInteger:
        expenses = paginator.page(1)
    except EmptyPage:
        expenses = paginator.page(paginator.num_pages)

    data = {
        "expenses": expenses,
        'yl': years_list,
        'ml': month_list,
        'dl': day_list,
        'cy': y, 'cm': m, 'cd': d
    }

    data_html = {
        'list': render_to_string('expense/list.htm', data),
    }
    return JsonResponse(data_html)

@auth.is_staff_required(redirect_url='expenses')
def add_expense(request):
    if 'HTTP_REFERER' in request.META:
        request.session['previous_url'] = request.META['HTTP_REFERER']
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
        return JsonResponse({ 'message': form.errors }, status=400)
    else:
        form = ExpenseForm()
        context = { 'form': form, 'page': "create_expense", 'page_name': 'Добавить расход' }
        return render(request, 'expense/form.htm', context)

@auth.is_staff_required(redirect_url='expenses')
def upd_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = ExpenseForm(instance=expense)
        context = { 'form': form, 'page': "edit_expense", 'page_name': 'Редактировать расход' }
        return render(request, 'expense/form.htm', context)

@auth.is_staff_required(redirect_url='expenses')
def del_expense(request):
    if request.method == "POST":
        expense = get_object_or_404(Expense, pk=request.POST.get('eID'))
        expense.delete()

        return JsonResponse({"status": "sucsess"})
    else:
        return Http404