from django.shortcuts import render
from .models import *
from .utils import cookieCart, cartData, questOrder

from django.http import JsonResponse
import json
import datetime
# Create your views here.

def Store(request):
   products = Product.objects.all()
   context = {'products': products}
   return render(request,
   'store/store.html', 
   context = context)

def Cart(request):
   data = cartData(request)
   items = data['items']
   order = data['order']

   context = {'items': items, 'order': order}
   return render(request,
   'store/cart.html', context = context)

def Checkout(request):
   data = cartData(request)
   items = data['items']
   order = data['order']

   context = {'items': items, 'order': order}
   return render(request,
   'store/checkout.html', context = context)

def CategoryProducts(request, text):
   products = Product.objects.filter(category__category = text)
   context = {'products': products}
   return render(request,
   'store/store_cat.html',
   context = context
   )

def updateCart(request):
   data = json.loads(request.body)
   productId = data['productId']
   action = data['action']
   # print(productId)
   product = Product.objects.get(id = productId)
   customer = request.user.customer
   order, created = Order.objects.get_or_create(customer=customer, complete=False)
   orderitem, created = OrderItem.objects.get_or_create(product=product, order=order) 

   if action == 'add':
      orderitem.quantity = orderitem.quantity + 1
   else:
      orderitem.quantity = orderitem.quantity - 1

   orderitem.save()

   if orderitem.quantity <= 0:
      orderitem.delete()

   return JsonResponse("siema", safe = False)

def processOrder(request):
   transaction_id = datetime.datetime.now().timestamp()
   data = json.loads(request.body)
   # print(data["form"]["name"])

   if request.user.is_authenticated:
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer=customer, complete = False)

   else:
      customer, order = questOrder(request, data)

   total = float(data["form"]["total"])
   order.transaction_id = transaction_id
   print(total)

   if total == order.get_cart_total:
      order.complete = True
   order.save()

   Shipping.objects.create(
      customer = customer,
      order = order,
      address = data['shipping']['address'],
      city = data['shipping']['city'],
      state = data['shipping']['state'],
      zip_code = data['shipping']['zip_code']
   )

   return JsonResponse("Order done", safe = False)