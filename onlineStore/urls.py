from django.http import HttpResponse
from django.urls import path, include
import django.contrib.auth.urls
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'onlineStore'

# the empty path '' becomes the 'home page
urlpatterns = [
        path('index', views.index, name='index'),
        path('', views.product_list, name='product_list'),
        path('accounts/', include('django.contrib.auth.urls')),
        path('basket_add/<int:product_id>/', views.basket_add, name ='basket_add'),
        path('basket_remove/<int:product_id>/', views.basket_remove, name ='basket_remove'),
        path('basket_detail/', views.basket_detail, name ='basket_detail'),
        path('signup/', views.signup, name='signup'),
        path('dashboard/', views.dashboard, name='dashboard'),
        path('customer_list/', views.customer_list, name='customer_list'),
        path('customer/<int:id>/', views.customer_detail, name= 'customer_detail'),
        path('order_list/', views.order_list, name='order_list'),
        path('order/<int:id>/', views.order_detail, name= 'order_detail'),
        path('payment/', views.payment, name ='payment'),
       # path('product/buy/', views.product_buy, name='product_buy'),
        #path('product_list/', views.product_list, name='product_list'),
        path('product/<int:id>/', views.product_detail, name= 'product_detail'),
        path('product_new/', views.product_new, name= 'product_new'),
        path('product/<int:id>/edit/', views.product_edit, name= 'product_edit'),
        path('product/<int:id>/delete/', views.product_delete, name= 'product_delete'),
        path('purchase/', views.purchase, name ='purchase'),
        path('search/', views.search, name='search'),
        ]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'onlineStore.views.handler404'
handler500 = 'onlineStore.views.handler500'