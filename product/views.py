from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.db.models import Q
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import *
from .tasks import *

from .forms import *

import auth


def my_products(request):
    data = {
        'page_name': 'Мои товары',
        'page': 'my_products',
    }
    return render(request, 'product/my_products.htm', data)

@auth.login_required(redirect_url='login')
def my_product_list(request):
    spp = request.GET.get('epp') if request.GET.get('epp') else 25
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    query = request.GET.get('q')

    if query:
        pList = MyProduct.objects.filter(Q(article__icontains=query) | Q(name__icontains=query))
    else:
        pList = MyProduct.objects.all().order_by('article')
    products = [
        {
            **model_to_dict(product),
            'image': product.image.url if product.image else None
        } for product in pList
    ]
    paginator = Paginator(products, spp)

    try:
        songs = paginator.page(page)
    except PageNotAnInteger:
        songs = paginator.page(1)
    except EmptyPage:
        songs = paginator.page(paginator.num_pages)

    data_html = {
        'list': render_to_string('product/my_list.htm', {"products": songs,}),
        'pagi': render_to_string('pagination.html', {"page": songs,})
    }
    return JsonResponse(data_html)

@auth.login_required(redirect_url='login')
def add_my_product(request):
    if request.method == "GET":
        data = {
            'page_name': 'Добавить продукт',
            "name": "add",
            "form": MyProductForm(),
        }
        return render(request, "product/forms/my_products.htm", data)
    elif request.method == "POST":
        form = MyProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('my_products')
        else:
            return JsonResponse({'message': form.errors}, status=400)
    else:
        return Http404

def upd_my_product(request, pID):
    if not pID: return Http404
    product = get_object_or_404(MyProduct, id=pID)

    if request.method == "GET":
        data = {
            'page_name': 'Редактировать продукт',
            'name': "update",
            'form': MyProductForm(instance=product),
            'product': product
        }
        return render(request, "product/forms/my_products.htm", data)
    elif request.method == "POST":
        form = MyProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            print(f"File saved to: {product.image.path}")
            return redirect('my_products')
        return JsonResponse({'message': form.errors}, status=400)
    else:
        return Http404

def del_my_product(request):
    if request.method == "POST":
        get_object_or_404(MyProduct, id=request.POST.get('pID')).delete()
        return JsonResponse({ 'status': 'success' })
    else:
        return Http404



# Create your views here.
@auth.login_required(redirect_url='login')
def products(request):
    suppliers = Supplier.objects.all().order_by('name')

    data = {
        'page_name': 'Товары поставщика',
        'page': 'sup_products',
        'suppliers': suppliers,
    }
    return render(request, 'product/products.htm', data)


@auth.login_required(redirect_url='login')
def product_list(request, sID):
    supplier = get_object_or_404(Supplier, id=sID)
    spp = request.GET.get('epp') if request.GET.get('epp') else 25
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    query = request.GET.get('q')

    if query:
        pList = supplier.supplier_products.filter(Q(article__icontains=query) | Q(name__icontains=query))
    else:
        pList = supplier.supplier_products.all().order_by('article')
    products = [{ **model_to_dict(product) } for product in pList ]
    paginator = Paginator(products, spp)

    try:
        songs = paginator.page(page)
    except PageNotAnInteger:
        songs = paginator.page(1)
    except EmptyPage:
        songs = paginator.page(paginator.num_pages)

    data_html = {
        'list': render_to_string('product/list.htm', {"products": songs,}),
        'pagi': render_to_string('pagination.html', {"page": songs,})
    }
    return JsonResponse(data_html)

@auth.login_required(redirect_url='login')
def import_sup_product(request):
    data = {
        'page_name': "Импортировать товар поставщика",
        'page': "import_sup_product"
    }
    return render(request, 'product/import/index.htm', data)

@auth.login_required(redirect_url='login')
def add_supplier(request):
    if request.method == "GET":
        data = {
            'page_name': 'Добавить поставщика',
            "name": "add",
            "form": SupplierForm(),
        }
        return render(request, "product/forms/supplier.htm", data)
    elif request.method == "POST":
        form = SupplierForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('import_sup_product')
        else:
            return JsonResponse({'message': form.errors}, status=400)
    else:
        return Http404

def upd_supplier(request, sID):
    if not sID: return Http404

    supplier = get_object_or_404(Supplier, id=sID)
    if request.method == "GET":
        data = {
            'page_name': 'Редактировать поставщика',
            "name": "update",
            "form": SupplierForm(instance=supplier),
            "supplier": supplier
        }
        return render(request, "product/forms/supplier.htm", data)
    elif request.method == "POST":
        form = SupplierForm(request.POST, request.FILES, instance=supplier)

        if form.is_valid():
            form.save()
            print(f"File saved to: {supplier.image.path}")
            return redirect('import_sup_product')
        return JsonResponse({'message': form.errors}, status=400)
    else:
        return Http404

def edit_supplier_auto_import(request):
    if request.method == "POST":
        supplier = get_object_or_404(Supplier, id=request.POST.get('id'))
        supplier.auto_import = True if request.POST.get('s') == 'true' else False
        supplier.save()

        return JsonResponse({ 'status': 'success' })
    else:
        return Http404

def del_supplier(request):
    if request.method == "POST":
        get_object_or_404(Supplier, id=request.POST.get('sID')).delete()
        return JsonResponse({ 'status': 'success' })
    else:
        return Http404

def sup_list(request):
    suppliers = Supplier.objects.all().order_by('name')

    return JsonResponse({ 'list': render_to_string('product/import/list.htm', { 'suppliers': suppliers }) })

def load_supplier_products(request, sID):
    if request.method == 'POST':
        supplier = get_object_or_404(Supplier, id=sID)
        fetch_supplier_data.delay(supplier.pk)
        return JsonResponse({ 'status': 'success' })
    else:
        return Http404