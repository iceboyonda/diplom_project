from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:tyre_id>/', views.cart_add, name='add'),
    path('remove/<int:tyre_id>/', views.cart_remove, name='remove'),
    path('update/<int:tyre_id>/', views.cart_update, name='update'),
    # URL-паттерны для дисков
    path('add-rim/<int:rim_variant_id>/', views.cart_add_rim, name='add_rim'),
    path('remove-rim/<int:rim_variant_id>/', views.cart_remove_rim, name='remove_rim'),
    path('update-rim/<int:rim_variant_id>/', views.cart_update_rim, name='update_rim'),
    path('clear/', views.cart_clear, name='clear'),
] 