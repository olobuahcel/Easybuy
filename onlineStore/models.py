from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.decorators.http import require_POST
from django import forms





# Create your models here.

class Products(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_type = models.CharField(max_length=200)
    brand        = models.CharField(max_length=200)
    price_usd   = models.FloatField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}, {self.product_type}, {self.brand}, {self.price_usd}, {self.created_date}"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    address = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email},{self.address}'

    class Meta:
        db_table = 'customer'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Customer.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.customer.save()
        

class LineItem(models.Model):
    #id = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField(default=1)
    product= models.ForeignKey('onlineStore.Products', on_delete=models.CASCADE, default=1)
    #product_type = models.ForeignKey('onlineStore.Products', on_delete=models.CASCADE)
    price_usd   = models.FloatField(default=0.00)
    cart = models.ForeignKey('onlineStore.Cart', on_delete=models.CASCADE)
    order = models.ForeignKey('onlineStore.Order', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity},{self.product}, {self.cart}, {self.price_usd}, {self.order},{self.created_date}'


class Cart(models.Model):
   
    product= models.ForeignKey('onlineStore.Products', on_delete=models.CASCADE, related_name='carts', default=1)
    quantity = models.IntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product},{self.quantity},{self.created_date}'


class Order(models.Model):
    customer = models.ForeignKey('onlineStore.Customer', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer},{self.created_date}'


