# inventory/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Transaction
from .forms import *
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
import csv
from django.http import HttpResponse

def product_list(request):
    products = Product.objects.all()
    return render(request, 'application/product_list.html', {'products': products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'application/product_form.html', {'form': form})

def stock_history(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    transactions = Transaction.objects.filter(product=product).order_by('-date')
    return render(request, 'application/stock_history.html', {'product': product, 'transactions': transactions})


def restock_product(request):
    if request.method == 'POST':
        form = RestockForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            amount = form.cleaned_data['amount']
            product = get_object_or_404(Product, id=product_id)
            product.restock(amount)
            return redirect('product_list')
    else:
        form = RestockForm()
    return render(request, 'application/restock_form.html', {'form': form})

def sell_product(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            amount = form.cleaned_data['amount']
            product = get_object_or_404(Product, id=product_id)
            try:
                product.sell(amount)
            except ValueError:
                # Handle error for insufficient stock
                return render(request, 'application/sale_form.html', {'form': form, 'error': 'Not enough stock available'})
            return redirect('product_list')
    else:
        form = SaleForm()
    return render(request, 'application/sale_form.html', {'form': form})


def current_stock_report(request):
    products = Product.objects.all()
    return render(request, 'application/current_stock_report.html', {'products': products})

def product_movement_report(request):
    today = timezone.now().date()
    start_date = today - timedelta(days=30)  # Last 30 days
    movements = Transaction.objects.filter(date__gte=start_date)
    return render(request, 'application/product_movement_report.html', {'movements': movements})

def sales_report(request, period):
    today = timezone.now().date()
    
    if period == 'daily':
        start_date = today
    elif period == 'weekly':
        start_date = today - timedelta(weeks=1)
    elif period == 'monthly':
        start_date = today - timedelta(days=30)
    else:
        # Default to daily if period is invalid
        start_date = today

    sales_movements = Transaction.objects.filter(transaction_type='sell', date__gte=start_date)
    total_sales = sales_movements.aggregate(total_quantity=Sum('quantity'))
    
    return render(request, 'application/sales_report.html', {
        'sales_movements': sales_movements,
        'total_sales': total_sales,
        'start_date': start_date,
        'end_date': today,
        'period': period
    })

def export_sales_report_csv(request, period):
    today = timezone.now().date()
    
    if period == 'daily':
        start_date = today
    elif period == 'weekly':
        start_date = today - timedelta(weeks=1)
    elif period == 'monthly':
        start_date = today - timedelta(days=30)
    else:
        # Default to daily if period is invalid
        start_date = today

    sales_movements = Transaction.objects.filter(transaction_type='sell', date__gte=start_date)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="sales_report_{period}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Product Name', 'Quantity', 'Date', 'Notes'])

    for movement in sales_movements:
        writer.writerow([movement.product.name, movement.quantity, movement.date, getattr(movement, 'notes', '')])

    return response
