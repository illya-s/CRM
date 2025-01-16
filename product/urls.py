from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(permanent=False, url='p/my/')),

    path('p/my/', views.my_products, name='my_products'),
    path('p/my/l/', views.my_product_list, name='my_product_list'),
    path('p/my/a/', views.add_my_product, name='add_my_product'),
    path('p/my/u/<int:pID>/', views.upd_my_product, name='upd_my_product'),
    path('p/my/d/', views.del_my_product, name='del_my_product'),

    path('p/', views.products, name='products'),
    path('p/l/<int:sID>', views.product_list, name='product_list'),

    path('s/import/', views.import_sup_product, name='import_sup_product'), # load_supplier_products
    path('s/import/load/<int:sID>', views.load_supplier_products, name='load_supplier_products'),
    path('s/l/', views.sup_list, name='sup_list'),
    path('s/a/', views.add_supplier, name='add_supplier'),
    path('s/e/<int:sID>', views.upd_supplier, name='upd_supplier'),
    path('s/e/import/', views.edit_supplier_auto_import, name='edit_supplier_auto_import'),
    path('s/d/', views.del_supplier, name='del_supplier'),

    # path('f/', views.product_forms, name='product_forms'),
    # path('', views. , name=''),
]