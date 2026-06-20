from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_expense, name='add_expense'),
    path('expenses/', views.expenses, name='expenses'),
    path('repay/<int:id>/', views.repay, name='repay'),
    path('logout/', views.logout_view, name='logout'),
    path('budget/', views.budget, name='budget'),
    path('export/', views.export_csv, name='export'),
    path('shared/', views.shared_expenses, name='shared'),
]