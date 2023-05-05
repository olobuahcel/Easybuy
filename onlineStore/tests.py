from django.test import TestCase

from django.test import TestCase
from django.contrib.auth.models import User
from onlineStore.models import Products, Customer, Cart, Order, LineItem

class OnlineStoreTestCase(TestCase):

    def setUp(self):
        # self.user = User.objects.create_user(username='testuser', password='testpass')
        # self.customer = Customer.objects.create(user=self.user, address='test_address')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # self.customer = Customer.objects.create(user=self.user, address='test_address')
        # self.product = Products.objects.create(product_type='test_product', brand='test_brand', price_usd=9.99)
        # self.cart = Cart.objects.create(product_id=self.product, quantity=2)
        # self.order = Order.objects.create(customer=self.customer)
        self.line_item = LineItem.objects.create(quantity=1, product_type=self.product, price_usd=9.99, cart=self.cart, order=self.order)

    # def test_products_model(self):
    #     product = Products.objects.get(product_type='test_product')
    #     self.assertEqual(str(product), f"'product.id', test_product, test_brand, 9.99, {product.created_date}")

    # def test_customer_model(self):
    #     try:
    #         customer = Customer.objects.create(user=self.user, address='test_address')
        
    #     except IntegrityError:
    #         customer = Customer.objects.get(user=self.user)
    #         self.assertEqual(str(customer), f"{self.user.email}, test_address")


    def test_cart_model(self):
        cart = Cart.objects.get(product_id=self.product)
        self.assertEqual(str(cart), f"'cart.product_id.id',{cart.quantity},{cart.created_date}")

    def test_order_model(self):
        order = Order.objects.get(customer=self.customer)
        self.assertEqual(str(order), f"{order.customer}, None, None, None, {order.created_date}")

    def test_line_item_model(self):
        line_item = LineItem.objects.get(cart=self.cart)
        self.assertEqual(str(line_item), f"{line_item.quantity},'line_item.product_type.product_type',{line_item.cart}, 9.99, {line_item.order},{line_item.created_date}")
# Create your tests here.
