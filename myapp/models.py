from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.CharField(max_length=100)
    rating = models.IntegerField()
    release_date = models.DateField(default=datetime.now)
    image_url = models.URLField()

    def __str__(self):
        return self.name

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order for {self.product} by {self.user.username}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in cart for {self.cart.user.username}"


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.CharField(max_length=100)
    rating = models.IntegerField()
    release_date = models.DateField(default=datetime.now)
    image_url = models.URLField()

    def __str__(self):
        return self.title
