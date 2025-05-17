from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='create'),
    path('', views.order_list, name='list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('admin-panel/orders/', views.admin_orders, name='admin_orders'),
    path('admin-panel/orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin-panel/orders/<int:order_id>/delete/', views.admin_order_delete, name='admin_order_delete'),
] 