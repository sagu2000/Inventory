# inventory/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/<int:product_id>/history/', views.stock_history, name='stock_history'),
    path('product/restock/', views.restock_product, name='restock_product'),
    path('product/sell/', views.sell_product, name='sell_product'),
    path('report/current_stock/', views.current_stock_report, name='current_stock_report'),
    path('report/product_movement/', views.product_movement_report, name='product_movement_report'),
    path('report/sales/<str:period>/', views.export_sales_report_csv, name='sales_report'),
    # path('admin/application/product/<int:pk>/change/',views.Change_product , name='change_product')
]
