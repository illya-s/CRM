from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', views.expenses, name="expenses"),
    path('l/', views.expense_list, name="expense_list"),
    
    path('c/l/', view=views.cat_list, name="cat_list"),
    path('c/a/', views.add_expense_cat, name="add_expense_cat"),
    path('c/u/<int:pk>/', views.upd_expense_cat, name="upd_expense_cat"),
    path('c/d/', views.del_expense_cat, name="del_expense_cat"),

    path('p/l/', view=views.plat_list, name="exp_plat_list"),
    path('p/a/', views.add_expense_plat, name="add_expense_plat"),
    path('p/u/<int:pk>/', views.upd_expense_plat, name="upd_expense_plat"),
    path('p/d/', views.del_expense_plat, name="del_expense_plat"),

    path('a/', views.add_expense, name='add_expense'),
    path('u/<int:pk>', views.upd_expense, name='upd_expense'),
    path('d/', views.del_expense, name="del_expense"),
]