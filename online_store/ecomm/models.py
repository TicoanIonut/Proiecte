from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	full_name = models.CharField(max_length=200)
	adress = models.CharField(max_length=200, null=True, blank=True)
	joined_on = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to='products')
	price = models.PositiveIntegerField()
	description = models.TextField()

	def __str__(self):
		return self.title
	
	
class Cart(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	total = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return 'Cart' + str(self.id)
	
	@property
	def get_cart_items(self):
		allitems = self.cartproduct_set.all()
		total = sum([product.quantity for product in allitems])
		return total


class CartProduct(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	rate = models.PositiveIntegerField()
	quantity = models.PositiveIntegerField()
	subtotal = models.PositiveIntegerField()
	
	def __str__(self):
		return	'Cart' + str(self.cart.id) + 'CartProduct: ' + str(self.id)
	

	
class Order(models.Model):
	cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
	ordered_by = models.CharField(max_length=200)
	shipping_adress = models.CharField(max_length=200)
	mobile = models.CharField(max_length=10)
	email = models.EmailField(null=True, blank=True)
	total = models.PositiveIntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return 'Order' + str(self.id)
	