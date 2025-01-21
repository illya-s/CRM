from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', views.orders, name='orders'),
    path('list/', views.order_list, name='order_list'),

    path('m/l/', views.get_model_list, name='get_model_list'),
    path('a/', views.add_order, name='create_order'),
    path('e/<int:pk>/', views.edit_order, name='edit_order'),
    path('d/', views.del_orders, name="del_orders"),


    # path('exp/', views.expenses, name="expenses"),
    # path('exp/list/', views.expense_list, name="expense_list"),

    # path('sender/a/', views.add_sender, name='add_sender'),
    # path('sender/d/', views.del_sender, name='del_sender')
]