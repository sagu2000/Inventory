# inventory/admin.py
from django.contrib import admin
from .models import Product, Transaction

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'quantity')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'transaction_type', 'date')
    list_filter = ('transaction_type', 'date')

# admin.site.register(Product,ProductAdmin)
# admin.site.register(Transaction,TransactionAdmin)
