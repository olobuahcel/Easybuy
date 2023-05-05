from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from onlineStore.forms import BasketAddProductForm, ProductForm
from decimal import Decimal
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from onlineStore.models import Cart, Customer, LineItem, Order, Products
from onlineStore.forms import SignUpForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *



def index(request):
    try:
        return render(request, 'onlineStore/index.html')
    except Exception as e:
        return render(request, 'onlineStore/error.html', {'error': 'Oops! Something went wrong.'})

def customer_list(request):
    try:
        users = User.objects.all()
        return render(request, 'onlineStore/customer_list.html', {'users' : users})
    except Exception as e:
        return render(request, 'onlineStore/error.html', {'error': 'Oops! Something went wrong.'})

def customer_detail(request, id):
    try:
        user = get_object_or_404(User, id=id)
        return render(request, 'onlineStore/customer_detail.html', {'user' : user})
    except Exception as e:
        return render(request, 'onlineStore/error.html', {'error': 'Oops! Something went wrong.'})

        
def order_list(request):
    try:
        orders = Order.objects.all()
        paginator = Paginator(orders, 10) # Show 10 orders per page
        page = request.GET.get('page')
        orders = paginator.get_page(page)
        return render(request, 'onlineStore/order_list.html', {'orders' : orders})   
    except Exception as e:
        return render(request, 'onlineStore/error.html', {'error': 'Oops! Something went wrong.'})


def order_detail(request, id):
    try:
        order = get_object_or_404(Order, id=id)
        customer = order.customer
        
        user = get_object_or_404(User, id=customer.pk)
        line_items = LineItem.objects.filter(order_id=order.id)
        return render(request, 'onlineStore/order_detail.html', {'order' : order, 'user': user, 'line_items': line_items})
    except Exception as e:
        return render(request, 'onlineStore/error.html', {'error': 'Oops! Something went wrong.'})

def signup(request):
    try:
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.customer.first_name = form.cleaned_data.get('first_name')
            user.customer.last_name = form.cleaned_data.get('last_name')
            user.customer.address = form.cleaned_data.get('address')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password= password)
            login(request, user)
            return redirect('/')
        return render(request, 'signup.html', {'form': form})
    except Exception as e:
        return render(request, 'onlineStore/error.html', {'error': 'Oops! Something went wrong.'})

@login_required
def dashboard(request):
    try:
        user = request.user
        if user.is_authenticated & user.is_staff:
            customers = Customer.object.all()
            order = Order.object.filter(customer__in=customers)
            data = []
            for customer in Customers:
                num_orders = orders.filter(customer= customer).count()
                data.append({
                    'customer_user' ==customer.user,
                    'num_orders' == num_orders,

                })
            return render(request, 'onlineStore/dashboard.html')
        else:
            return redirect('/accounts/login.html')
    except Exception as e:
        return render(request, 'onlineStore/error.html', {'error': 'Oops! Something went wrong.'})


# save order, clear basket and thank customer
def payment(request):
    try:
        basket = Basket(request)
        user = request.user
        customer = get_object_or_404(Customer, user_id=user.id)
        order = Order.objects.create(customer=customer)
        order.refresh_from_db()
        for item in basket:
            product_item = get_object_or_404(Products, id=item['product_id'])
            cart = Cart.objects.create(product = product_item, quantity=item['quantity'])
            cart.refresh_from_db()
            line_item = LineItem.objects.create(quantity=item['quantity'], product=product_item, cart=cart,  order = order)

        basket.clear()
        request.session['deleted'] = 'thanks for your purchase'
        return redirect('onlineStore:product_list' )
    except Exception as e:
        return render(request, 'onlineStore/error.html', {'error': 'Oops! Something went wrong.'})

def purchase(request):
    try:
        if request.user.is_authenticated:
            user = request.user
            basket = Basket(request)
       
            return render(request, 'onlineStore/purchase.html', {'basket': basket, 'user': user})
        else:
            return redirect('onlineStore:dashboard')
            # return redirect('login')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('home')

# def product_list(request):
#     products = Products.objects.all()    
#     return render(request, 'onlineStore/product_list.html', {'products' : products })




def product_list(request):
    try:
        product_list = Products.objects.all()
        paginator = Paginator(product_list, 10) # 10 items per page

        page = request.GET.get('page')
        products = paginator.get_page(page)

        return render(request, 'onlineStore/product_list.html', {'products': products})
    except Exception as e:
        return render(request, 'onlineStore/error.html', {'error': 'Oops! Something went wrong.'})

def product_detail(request, id):
    try:
        product = get_object_or_404(Products, id=id)
        basket_product_form = BasketAddProductForm()
        return render(request, 'onlineStore/product_detail.html', {'product' : product, 'basket_product_form': basket_product_form })
    except Exception as e:
        return render(request, 'onlineStore/error.html', {'error': 'Oops! Something went wrong.'})

def product_new(request):
    try:
        if request.method=="POST":
            form = ProductForm(request.POST)
            if form.is_valid():
                product = form.save(commit=False)
                product.created_date = timezone.now()
                product.save()
                return redirect('onlineStore:product_detail', id=product.id)
        else:
            form = ProductForm()
        return render(request, 'onlineStore/product_edit.html', {'form': form})
    except Exception as e:
        return render(request, 'onlineStore/error.html', {'error': 'Oops! Something went wrong.'})

def product_edit(request, id):
    try:
        product = get_object_or_404(Products, id=id)
        if request.method=="POST":
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                product = form.save(commit=False)
                product.created_date = timezone.now()
                product.save()
                return redirect('onlineStore:product_detail', id=product.id)
            
        else:
            form = ProductForm(instance=product)
        return render(request, 'onlineStore/product_edit.html', {'form': form})
    except Exception as e:
        return render(request, 'onlineStore/error.html', {'error': 'Oops! Something went wrong.'})


def product_delete(request, id):
    try:
        product = get_object_or_404(Products, id=id)
        deleted = request.session.get('deleted', 'empty')
        request.session['deleted'] = product.id
        product.delete()
        return redirect('onlineStore:product_list' )
    except Exception as e:
        return render(request, 'onlineStore/error.html', {'error': 'Oops! Something went wrong.'})

class Basket(object):
    # a data transfer object to shift items from cart to page
    # inspired by Django 3 by Example (2020) by Antonio Mele
    # https://github.com/PacktPublishing/Django-3-by-Example/
    
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            # save an empty basket in the session
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def __iter__(self):
        """
        Iterate over the items in the basket and get the products
        from the database.
        """
        print(f'basket: { self.basket }')
        product_ids = self.basket.keys()
        # get the product objects and add them to the basket
        products = Products.objects.filter(id__in=product_ids)

        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product
            basket[str(product.id)]['product_id'] = product.id

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the basket.
        """
        return sum(item['quantity'] for item in self.basket.values())

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the basket or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'quantity': 0,
                                      'price': str(product.price_usd)}
        if override_quantity:
            self.basket[product_id]['quantity'] = quantity
        else:
            self.basket[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the basket.
        """
        product_id = str(product.id)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def clear(self):
        # remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())


@require_POST
def basket_add(request, product_id):
    try:
        basket = Basket(request)
        product = get_object_or_404(Products, id=product_id)
        form = BasketAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            basket.add(product=product,
                    quantity=cd['quantity'],
                    override_quantity=cd['override'])
        return redirect('onlineStore:basket_detail')
    except Exception as e:
        return render(request, 'onlineStore/error.html', {'error': 'Oops! Something went wrong.'})    

@require_POST
def basket_remove(request, product_id):
    try:
        basket = Basket(request)
        product = get_object_or_404(Products, id=product_id)
        basket.remove(product)
        return redirect('onlineStore:basket_detail')
    except Exception as e:
        return render(request, 'onlineStore/error.html', {'error': 'Oops! Something went wrong.'})

def basket_detail(request):
    try:
        basket = Basket(request)
        for item in basket:
            item['update_quantity_form'] = BasketAddProductForm(initial={'quantity': item['quantity'],
                                                                    'override': True})
        return render(request, 'onlineStore/basket.html', {'basket': basket})
    except Exception as e:
        return render(request, 'onlineStore/error.html', {'error': 'Oops! Something went wrong.'})



def search(request):
    query = request.GET.get('q')
    if query:
        # Search all the models in models.py
        results = (
            Products.objects.filter(Q(product_type__icontains=query) | Q(brand__icontains=query) | Q(price_usd__icontains=query)) |
            Customer.objects.filter(Q(user__username__icontains=query) | Q(address__icontains=query)) |
            LineItem.objects.filter(Q(quantity__icontains=query) | Q(product__product_type__icontains=query) | Q(product__brand__icontains=query) | Q(price_usd__icontains=query)) |
            Cart.objects.filter(Q(quantity__icontains=query) | Q(product__product_type__icontains=query) | Q(product__brand__icontains=query)) |
            Order.objects.filter(Q(customer__user__username__icontains=query))
        )
        context = {
            'results': results,
            'query': query
        }
        return render(request, 'search.html', context)
    else:
        return render(request, 'search.html')

          
# def search(request):
#     try:
#         if 'q' in request.GET:
#             q = request.GET['q']
#             multiple_q= Q(Q(id__icontains=q) | Q(product_type__icontains=q) | Q(brand__icontains=q) | Q(price_usd__icontains=q))
#             products = Products.objects.filter(multiple_q)

#         else:
#             product= Products.object.all()    
#             context = {'products': products}
#         return render(request, 'onlineStore/search.html', context)
#     except Exception as e:
#         return render(request, 'onlineStore/error.html', {'error': 'Oops! Something went wrong.'})



def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)




