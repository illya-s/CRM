from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse, Http404
from django.forms.models import model_to_dict
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import *
from .forms import *
from .tasks import *

from datetime import timedelta
from django.utils import timezone

import requests, auth
from config import np_url, api_key


@auth.login_required(redirect_url='login')
def orders(request):
    payments = [
        { "val": i, "name": v }
        for i, v in Order.PAYMENTS
    ]
    data = {
        "page": "orders",
        "payments": payments
    }
    
    return render(request, 'order/orders.htm', data)


# def get_ttn_data(ttn_list:list):
#     headers = { 'Content-Type': 'application/json', 'Api-Key': api_key }

#     tl = [ { "DocumentNumber": ''.join(ttn.split(" ")) } for ttn in ttn_list if ttn is not None ]
#     # ttn_list = list(filter(lambda x: x is not None, my_list))
#     if not tl:
#         return [None] * len(ttn_list)

#     data = {
#         "modelName": "TrackingDocumentGeneral",
#         "calledMethod": "getStatusDocuments",
#         "methodProperties": {
#             "Documents": tl
#         }
#     }
#     response = requests.get(np_url, json=data, headers=headers)

#     ststus = []

#     if response.status_code == 200:
#         for el in response.json()['data']:
#             if el["StatusCode"] == "1":
#                 st = "Очікування відправки"
#             elif el["StatusCode"] in ["9", "10", "11"]:
#                 st = "Отримано"
#             else:
#                 st = el["Status"]
#             ststus.append({ "code": el["StatusCode"], "name": st })
#     else:
#         ststus = None

#     return ststus


np_ttn_url = "https://novaposhta.ua/tracking/?cargo_number=" # 20 0200 0035 8250
olx_ttn_url = "https://track.ukrposhta.ua/tracking_UA.html?barcode=" # 73 0200 0035 825

def get_clear_ttn(ttn:str):
    return ''.join(str(ttn).split(' '))
def is_np_ttn(ttn:str):
    return True if len(get_clear_ttn(ttn)) == 14 else False


def order_list(request):
    if request.method == "GET":
        spp = request.GET.get('epp') if request.GET.get('epp') else 25
        page = int(request.GET.get('page')) if request.GET.get('page') else 1

        orders_obj = [
            {
                **model_to_dict(order),
                "product": model_to_dict(order.product) if order.product else None,
                "ttnLink": (
                    f"{np_ttn_url}{get_clear_ttn(order.ttn)}" if is_np_ttn(order.ttn) else f"{olx_ttn_url}{get_clear_ttn(order.ttn)}"
                ),
                "payment": order.get_payment_display(),
                "updated": order.updated.strftime("%d.%m.%y") if order.updated else None,
                "income": order.income()
            }
            for order in Order.objects.all().order_by("-id")
        ]
        paginator = Paginator(orders_obj, spp)

        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)

        data = {
            "orders": orders,
        }

        data_html = {
            'list': render_to_string('order/list.htm', data),
            'pagi': render_to_string('pagination.html', { "page": orders }),
        }
        return JsonResponse(data_html)
    else:
        return Http404


# @auth.login_required(redirect_url='login')
def get_model_list(request):
    if request.method == "GET":
        content_type = get_object_or_404(ContentType, id=request.GET.get('mID'))
        model_class = content_type.model_class()
        mls = model_class.objects.all()
        return JsonResponse({"models": [ {'id': ml.id, 'name': str(ml)} for ml in mls ]})
    else:
        return Http404


@auth.login_required(redirect_url='login')
def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            get_ttn_status.delay(instance.pk)
            return redirect('orders')
        return JsonResponse({ 'message': form.errors }, status=400)
    else:
        form = OrderForm()
        context = {
            'form': form,
            'page': "create_order"
        }
        return render(request, 'order/form.htm', context)

@auth.login_required(redirect_url='login')
def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            instance = form.save()
            get_ttn_status.delay(instance.pk)
            return redirect('orders')
    else:
        form = OrderForm(instance=order)
    return render(request, 'order/form.htm', {'form': form, 'page': "edit_order"})


# def export_orders(request, type):
#     model = Order.objects.all()
#     if type in ['xml', 'json', 'yaml']:
#         data = serializers.serialize(type, model)
#         response = HttpResponse(data, content_type=f'application/{type}')
#         response['Content-Disposition'] = f'attachment; filename="data.{type}"'
#         return response
#     elif type == 'csv':
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="data.csv"'

#         writer = csv.writer(response)
#         writer.writerow(["Ім'я", 'Прізвище', 'Телефон', "Статус", "TTN", "Оплата", "Створено", "Оновлено"])
#         for obj in model:
#             writer.writerow([obj.client_name, obj.client_surname, obj.client_phone, obj.status, obj.ttn, obj.payment, obj.created, obj.updated])
#         return response
#     else:
#         return HttpResponse("type error", 404)

@auth.login_required(redirect_url='login')
def del_orders(request):
    if request.method == "GET":
        ids = request.GET.get('ids')
        for el in ids.split(","):
            get_object_or_404(Order, id=int(el)).delete()

        return JsonResponse({"status": "sucsess"})
    else:
        return Http404



def import_orders(request):
    return render(request, "order/import.htm")


@auth.login_required(redirect_url='login')
def statistic(request):
    today = datetime.datetime.now()
    year_ago = datetime.datetime(today.year, 1, 1)

    one_month_ago = today - timedelta(days=30)
    
    most_purchased_products = (
        Product.objects.annotate(order_count=Count('order'))
        .order_by('-order_count')[:5]
    )
    products_data = [
        {'name': product.article if product.article else product.name, 'order_count': product.order_count}
        for product in most_purchased_products
    ]

    sup_mpp = (
        Supplier.objects.annotate(product_count=Count('supplier_products'))
        .order_by('-product_count')[:5]
    )
    sup_data = [
        {'name': supplier.name, 'product_count': supplier.product_count}
        for supplier in sup_mpp
    ]

    sales_data = (
        Order.objects.filter(date__range=(year_ago, today))
        .annotate(day=TruncDate('date'))
        .values('day')
        .annotate(total_sales=Sum('amount'))
        .order_by('day')
    )
    all_dates = [(year_ago + timedelta(days=i)).date().strftime('%d.%m') for i in range((today - year_ago).days + 1)]
    sales_dict = {item['day'].strftime('%d.%m'): item['total_sales'] for item in sales_data}

    filled_sales_data = [
        {'day': date, 'total_sales': sales_dict.get(date, 0)} for date in all_dates
    ]
    filled_sales_data.reverse()

    context = {
        'orders': [{ **model_to_dict(order) } for order in Order.objects.filter(date__gte=one_month_ago)],
        'products_data': products_data,
        'sup_data': sup_data,
        'by_day': filled_sales_data
    }
    return render(request, 'order/statistic/index.htm', context)



# @auth.login_required(redirect_url='login')
# def expenses(request):
#     data = {
#         "page": "expenses",
#     }
    
#     return render(request, 'expense/expenses.htm', data)


# def expense_list(request):
#     if request.method == "GET":
#         spp = request.GET.get('epp') if request.GET.get('epp') else 25
#         page = int(request.GET.get('page')) if request.GET.get('page') else 1

#         expense_objs = [
#             {
#                 **model_to_dict(expense),
#                 "created": expense.created.strftime("%d.%m.%y"),
#                 "product": {
#                     "id": expense.product.id,
#                     "name": expense.product.name
#                 } if expense.product else None,
#                 "type": expense.type.name if expense.type else None,
#             }
#             for expense in Expense.objects.all()
#         ]
#         paginator = Paginator(expense_objs, spp)

#         try:
#             expense = paginator.page(page)
#         except PageNotAnInteger:
#             expense = paginator.page(1)
#         except EmptyPage:
#             expense = paginator.page(paginator.num_pages)

#         data = {
#             "expenses": expense,
#         }

#         data_html = {
#             'list': render_to_string('expense/list.htm', data),
#             'pagi': render_to_string('pagination.html', { "page": expense }),
#         }
#         return JsonResponse(data_html)
#     else:
#         return Http404


# @auth.login_required(redirect_url='login')
# def add_sender(request):
#     if request.method == 'POST':
#         form = SenderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('orders')
#     else:
#         form = SenderForm()
#     return render(request, 'order/sender/form.htm', {'form': form, 'page': "create_order_sender"})

# @auth.login_required(redirect_url='login')
# def del_sender(request):
#     if request.method == "GET":
#         ids = request.GET.get('ids')
#         for el in ids.split(","):
#             get_object_or_404(Sender, id=int(el)).delete()

#         return JsonResponse({"status": "sucsess"})
#     else:
#         return Http404
