from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),  # Login page
    path('reg/', views.reg, name='reg'),  # Registration page
    path('', views.login, name='login'),  # Redirect root to login page
    path('home/', views.home, name='home'),  # Home page after login
    path('create/', views.create_account, name='create'),  # Create account page
    path('withdraw/', views.withdraw, name='withdraw'),  # Withdraw page
    path('deposit/', views.deposit, name='deposit'),  # Deposit page
    path('check_balance/', views.check_balance, name='check_balance'),  # Check balance page
    path('transaction_history/', views.transaction_history, name='transaction_history'),  # Transaction history
    path('logout/', views.logout_view, name='logout'),
    path('create_acount/', views.create_account, name='create_account'),

]
