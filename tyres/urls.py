from django.urls import path
from . import views

app_name = 'tyres'

urlpatterns = [
    path('', views.catalogue, name='catalogue'),
    path('tyre/<int:tyre_id>/', views.tyre_detail, name='tyre_detail'),
    path('search/', views.search_tyres, name='search_tyres'),
    path('faq/', views.faq, name='faq'),
    path('favourite/add/<int:variant_id>/', views.add_favourite, name='add_favourite'),
    path('favourite/remove/<int:variant_id>/', views.remove_favourite, name='remove_favourite'),
    path('favourites/', views.favourites, name='favourites'),
    path('admin-panel/tyres/', views.admin_tyres, name='admin_tyres'),
    path('admin-panel/tyres/add/', views.admin_tyre_add, name='admin_tyre_add'),
    path('admin-panel/tyres/<int:tyre_id>/edit/', views.admin_tyre_edit, name='admin_tyre_edit'),
    path('admin-panel/tyres/<int:tyre_id>/delete/', views.admin_tyre_delete, name='admin_tyre_delete'),
    path('admin-panel/categories/', views.admin_categories, name='admin_categories'),
    path('rims/', views.rim_list, name='rim_list'),
    path('rims/<int:rim_id>/', views.rim_detail, name='rim_detail'),
    path('favourite-rim/add/<int:variant_id>/', views.add_favourite_rim, name='add_favourite_rim'),
    path('favourite-rim/remove/<int:variant_id>/', views.remove_favourite_rim, name='remove_favourite_rim'),

    # URL-адреса для управления дисками в админ-панели
    path('admin-panel/rims/', views.admin_rims, name='admin_rims'),
    path('admin-panel/rims/add/', views.admin_rim_add, name='admin_rim_add'),
    path('admin-panel/rims/<int:rim_id>/edit/', views.admin_rim_edit, name='admin_rim_edit'),
    path('admin-panel/rims/<int:rim_id>/delete/', views.admin_rim_delete, name='admin_rim_delete'),
] 