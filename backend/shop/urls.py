from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('auth/csrf/', views.csrf_token, name='csrf-token'),
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/me/', views.current_user, name='current-user'),
    path('auth/google/', views.google_login, name='google-login'),
    path('orders/', views.order_list, name='order-list'),
    path('orders/create/', views.create_order, name='order-create'),
]
