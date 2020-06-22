import json
from .models import *

def cookieCart(request):
   try:
      cart = json.loads(request.COOKIES['cart'])
   except:
      cart = {}
   print('Cart:', cart)
   order = {'get_cart_items': 0, 'get_cart_total': 0}
   # cartItems = order['get_cart_items']
   items = []
   for i in cart:
      #try prevents error when product will be removed from database
      try:
         # cartItems += cart[i]['quantity']
         product = Product.objects.get(id=i)
         total = (product.prize * cart[i]['quantity'])

         order['get_cart_total'] += total
         order['get_cart_items'] += cart[i]['quantity']

         item = {#ręczne stworzenie elementów produktu
            'product':{
               'id': product.id,
               'name': product.name,
               'price': product.prize,
               'imageURL': product.imageURL
            },
            'quantity': cart[i]['quantity'],
            'get_total': total
         }
         items.append(item)
      except:
         pass
   return {'order': order, 'items': items}


def cartData(request):
   if request.user.is_authenticated:
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer = customer, complete = False)
      items = order.orderitem_set.all()
   else:
      cookieData = cookieCart(request)
      items = cookieData['items']
      order = cookieData['order']
   return{'order': order, 'items':items}

def questOrder(request, data):
   print('User is not logged in ..')
   print('COOKIES:', request.COOKIES)
   email = data["form"]["email"]
   name = data["form"]["name"]
   print('Name:',name, email)

   cookieData = cookieCart(request)
   items = cookieData['items']

   customer, created = Customer.objects.get_or_create(email=email,)
   customer.name = name
   customer.save()

   order = Order.objects.create(
      customer = customer,
      complete = False
   )

   for item in items:
      product = Product.objects.get(id = item['product']['id'])

      orderItem = OrderItem.objects.create(
         product = product,
         order = order,
         quantity = item['quantity']
      )

   return customer, order