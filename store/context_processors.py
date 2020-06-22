from django.shortcuts import render
from .models import Category, Customer, Order, Product
import json


def cat_on_all_pages(request):
    return {'categories': Category.objects.all(),
    'request': request}

def cartItems(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        cartItems = order.get_cart_items

    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        order = {'get_cart_items': 0}
        cartItems = order['get_cart_items']
        for i in cart:
            cartItems += cart[i]['quantity']

    return {'cartItems': cartItems,
    'request': request}