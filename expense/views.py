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
        context = { 'form': form, 'page': "create_expense_category", 'page_name': 'Добавить категорию расходов' }
        return render(request, 'expense/form.htm', context)
@auth.is_staff_required(redirect_url='expenses')
def del_expense_cat(request):
    if request.method == 'POST':
        expense_cat = get_object_or_404(ExpenseCategory, pk=request.POST.get('cID'))
        expense_cat.delete()

        return JsonResponse({ 'message': 'sucses' }, status=200)
    else:
        return Http404


def expense_list(request):
    if request.method != "GET":
        return Http404
    spp = request.GET.get('epp') if request.GET.get('epp') else 25
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    f = request.GET.get('filter')

    if f != "-1":
        eCat = get_object_or_404(ExpenseCategory, id=f)
        objs = eCat.category_expenses.all()
    else:
        objs = Expense.objects.all()

    expenses_obj = [
        {
            **model_to_dict(order),
            'expense': order.expense.name
        }
        for order in objs.order_by("-date")
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
    }

    data_html = {
        'list': render_to_string('expense/list.htm', data),
        'pagi': render_to_string('pagination.html', { "page": expenses }),
    }
    return JsonResponse(data_html)

@auth.is_staff_required(redirect_url='expenses')
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('expenses')
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
            return redirect('expenses')
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