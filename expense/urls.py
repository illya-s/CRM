from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', views.expenses, name="expenses"),
    path('l/', views.expense_list, name="expense_list"),

    path('a/', views.add_expense, name='add_expense'),
    path('e/', views.upd_expense, name='upd_expense'),
    path('d/', views.del_expense, name="del_expense"),
]