from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
   user = models.OneToOneField(User, null=True, blank = True, on_delete = models.CASCADE)
   name = models.CharField(max_length=100, null = True)
   email = models.CharField(max_length=100, null = True)

   def __str__(self):
      return self.email

class Category(models.Model):
   category = models.CharField(max_length=100, verbose_name= "Kategoria")

   def __str__(self):
      return self.category

class Product(models.Model):
   category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True, verbose_name= "Kategoria")
   name = models.CharField(max_length=200, verbose_name= "Nazwa produktu")
   prize = models.DecimalField(max_digits=7, decimal_places=2, null = True, verbose_name= "Cena")
   digital = models.BooleanField(default=False)
   image = models.ImageField(null = True, verbose_name= "Obraz")

   def __str__(self):
      return self.name
   
   @property
   def imageURL(self):
      try:
         url = self.image.url
      except:
         url = ''
      return url

class Order(models.Model):#koszyk
   customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
   date_ordered = models.DateTimeField(auto_now_add=True, null = True)
   transaction_id = models.IntegerField(verbose_name= "Numer zamówienia", null = True)
   complete = models.BooleanField(default=False, verbose_name= "Wykonane")

   def __str__(self):
      return str(self.transaction_id)

   # @property
   # def shipping(self):
   #    shipping = 'False'
   #    orderitem = self.orderitem_set.all()
   #    for i in orderitem:
   #       if i.product.digital 
   
   @property
   def get_cart_total(self):
      items = self.orderitem_set.all()
      total = sum([item.get_total for item in items])
      return total
   
   @property
   def get_cart_items(self):
      items = self.orderitem_set.all()
      total = sum([item.quantity for item in items])
      return total

class OrderItem(models.Model):#produkt w naszym koszyku
   order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True, blank = True, verbose_name= "Numer zamówienia")#order może mieć wiele orderitem
   product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True, blank = True, verbose_name= "Produkt")#Produkt może być wielokrotnie jako orderitem
   quantity = models.IntegerField(verbose_name= "Ilość", default= 0)
   date_added = models.DateTimeField(auto_now_add=True, null = True)

   @property
   def get_total(self):
      total = self.quantity * self.product.prize
      return total


class Shipping(models.Model):
   customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null = True, blank = True)
   order = models.ForeignKey(Order, on_delete=models.SET_NULL, null = True, blank = True)
   address = models.CharField(max_length=200, null = True)
   city = models.CharField(max_length=200, null = True)
   state = models.CharField(max_length=200, null = True)
   zip_code = models.CharField(max_length=200, null = True)