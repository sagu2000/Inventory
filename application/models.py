from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def restock(self, amount):
        self.quantity += amount
        self.save()
        Transaction.objects.create(product=self, quantity=amount, transaction_type='restock')

    def sell(self, amount):
        if amount > self.quantity:
            raise ValueError("Not enough stock available")
        self.quantity -= amount
        self.save()
        Transaction.objects.create(product=self, quantity=-amount, transaction_type='sell')

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('restock', 'Restock'),
        ('sell', 'Sell'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.transaction_type} - {self.product.name} - {self.quantity}"

