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
def product_list(request):
    # supplier = get_object_or_404(Supplier, id=sID)
    spp = request.GET.get('epp') if request.GET.get('epp') else 25
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    query = request.GET.get('q')

    if query:
        pList = Product.objects.filter(Q(article__icontains=query) | Q(name__icontains=query))
    else:
        pList = Product.objects.all().order_by('article')
    products = [
        {
            **model_to_dict(product),
            'supplier': str(product.supplier)
        }
        for product in pList
    ]
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


def sup_availability(request, pk):
    supplier = get_object_or_404(Supplier, id=pk)
    products = supplier.supplier_products.all() #.products_availability.all()
    # products_amount = products.products_amount.all()

    data = {
        'page_name': f'Наличие обувь - {supplier.name}',
        "products": products,
    }
    
    return render(request, 'product/availability/availability.htm', data)


@auth.login_required(redirect_url='login')
def add_product(request):
    if request.method == "GET":
        data = {
            'page_name': 'Добавить продукт',
            "name": "add",
            "form": ProductForm(),
        }
        return render(request, "product/forms/products.htm", data)
    elif request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('products')
        else:
            return JsonResponse({'message': form.errors}, status=400)
    else:
        return Http404

def upd_product(request, pID):
    if not pID: return Http404
    product = get_object_or_404(Product, id=pID)

    if request.method == "GET":
        data = {
            'page_name': 'Редактировать продукт',
            'name': "update",
            'form': ProductForm(instance=product),
            'product': product
        }
        return render(request, "product/forms/products.htm", data)
    elif request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            print(f"File saved to: {product.image.path}")
            return redirect('products')
        return JsonResponse({'message': form.errors}, status=400)
    else:
        return Http404

def del_product(request):
    if request.method == "POST":
        get_object_or_404(Product, id=request.POST.get('pID')).delete()
        return JsonResponse({ 'status': 'success' })
    else:
        return Http404