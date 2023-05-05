from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Customer, Products, Order, LineItem, Cart 

# Register your models here.
admin.site.register(Products)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(LineItem)
admin.site.register(Cart)