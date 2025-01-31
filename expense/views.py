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
    return render(request, 'expense/expenses.htm')

def expense_list(request):
    if request.method == "GET":
        spp = request.GET.get('epp') if request.GET.get('epp') else 25
        page = int(request.GET.get('page')) if request.GET.get('page') else 1

        expenses_obj = [
            {
                **model_to_dict(order),
                'expense': order.expense.name
            }
            for order in Expense.objects.all().order_by("-date")
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
    else:
        return Http404

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
def upd_expense(request):
    if request.method == 'POST':
        expense = get_object_or_404(Expense, pk=request.POST.get('eID'))
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expenses')
    else:
        expense = get_object_or_404(Expense, pk=request.GET.get('eID'))
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