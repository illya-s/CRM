from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(permanent=False, url='p/')),

    # path('p/my/', views.my_products, name='my_products'),
    # path('p/my/l/', views.my_product_list, name='my_product_list'),

    path('p/', views.products, name='products'),
    path('p/l/', views.product_list, name='product_list'),

    path('s/import/', views.import_sup_product, name='import_sup_product'), # load_supplier_products
    path('s/import/load/<int:sID>', views.load_supplier_products, name='load_supplier_products'),

    path('s/l/', views.sup_list, name='sup_list'),
    path('s/a/<int:pk>/', views.sup_availability, name='sup_availability'),
    
    path('s/a/', views.add_supplier, name='add_supplier'),
    path('s/e/<int:sID>', views.upd_supplier, name='upd_supplier'),
    path('s/e/import/', views.edit_supplier_auto_import, name='edit_supplier_auto_import'),
    path('s/d/', views.del_supplier, name='del_supplier'),

    path('p/a/', views.add_product, name='add_product'),
    path('p/u/<int:pID>/', views.upd_product, name='upd_product'),
    path('p/d/', views.del_product, name='del_product'),

    # path('f/', views.product_forms, name='product_forms'),
    # path('', views. , name=''),
]