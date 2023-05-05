from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from datetime import datetime
from django.db import models
from pathlib import Path
from faker import Faker
import random
import decimal
import csv
import os

from onlineStore.models import Cart, Customer, LineItem, Order, Products

class Command(BaseCommand):
    help = 'Load data from csv'

    def handle(self, *args, **options):


        Cart.objects.all().delete()
        LineItem.objects.all().delete()
        Order.objects.all().delete()
        Products.objects.all().delete()
        Customer.objects.all().delete()
        User.objects.all().delete()
        print("tables dropped successfully")


        # drop the data from the table so that if we rerun the file, we don't repeat values
        Products.objects.all().delete()
        print("table dropped successfully")
        
        # create table again

        # open the file to read it into the database
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        with open(str(base_dir) + '/onlineStore/BigBasketProducts.csv', newline='') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader) # skip the header line
            for row in reader:
                print(row)

                product = Products.objects.create(
                id = int(row[0]),
                product_type = row[7],
                brand = row[4],
                price_usd = float(row[6]),
                )
                product.save()
        print("data parsed successfully")

                
        fake = Faker()

        # create some customers
        # we convert some values from tuples to strings
        for i in range(10):
            first_name = fake.first_name(),
            first_name = str(first_name[0])
            last_name = fake.last_name(),
            last_name = str(last_name[0])
            username = first_name + last_name,
            username = username[0]
            user = User.objects.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = fake.ascii_free_email(), 
            password = 'p@ssw0rd')
            customer = Customer.objects.get(user = user)
            customer.address = fake.address(),
            customer.address = str(customer.address[0])
            customer.save()

        # create some products
        # for i in range(10):
        #     product = Products.objects.create(
        #     name = fake.catch_phrase(),
        #     price = int( decimal.Decimal(random.randrange(155,899))/100),
        #     )
        #     product.save()

        # create some carts 
        products = list(Products.objects.all())
        for i in range(10):
            random_id = random.randint(1,9)
            cart = Cart.objects.create(
            product = products[random_id],
            quantity = random.randrange(1,42),
            )
            cart.save()

        # create orders from customers
        customers = Customer.objects.all()
        for customer in customers:  
            for i in range(3):
                order = Order.objects.create(
                customer = customer,
                )
                order.save()
               
        # attach line_items to orders
        orders = Order.objects.all()
        carts = Cart.objects.all()
        for order in orders:
            for cart in carts:
                line_item = LineItem.objects.create(
                quantity = cart.quantity,
                product = cart.product,
                cart = cart,
                order = order,
                )
                line_item.save()
        
        print("tables successfully loaded")