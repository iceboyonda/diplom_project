from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:tyre_id>/', views.cart_add, name='add'),
    path('remove/<int:tyre_id>/', views.cart_remove, name='remove'),
    path('update/<int:tyre_id>/', views.cart_update, name='update'),
] 