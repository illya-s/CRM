from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
    path('edit_user/<int:uID>/', views.upd_user, name='edit_user'),

    path('profile/', views.profile, name='profile'),
]
