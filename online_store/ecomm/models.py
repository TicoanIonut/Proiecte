from django.db import models
from django.contrib.auth.models import User


class Admin(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	full_name = models.CharField(max_length=50)
	image = models.ImageField(upload_to='admins')
	mobile = models.CharField(max_length=50)
	
	def __str__(self):
		return self.user.username


class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	full_name = models.CharField(max_length=200)
	address = models.CharField(max_length=200, null=True, blank=True)
	joined_on = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to='products')
	price = models.PositiveIntegerField()
	description = models.TextField()
	view_count = models.PositiveIntegerField(default=0)

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
		if total == 0:
			total = 0
			return total
		return total
	
	@property
	def get_cart_total(self):
		totalitems = self.cartproduct_set.all()
		tot = sum([product.get_total for product in totalitems])
		return tot


class CartProduct(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	rate = models.PositiveIntegerField()
	quantity = models.PositiveIntegerField()
	subtotal = models.PositiveIntegerField()
	
	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total
	
	def __str__(self):
		return 'Cart' + str(self.cart.id) + 'CartProduct: ' + str(self.id)
	
	
ORDER_STATUS = (
	("Order Received", "Order Received"),
	("Order Processing", "Order Processing"),
	("On the way", "On the way"),
	("Order Completed", "Order Completed"),
	("Order Canceled", "Order Canceled"),
)

METHOD = (
	("Cash On Delivery", "Cash On Delivery"),
	("PayU", "PayU"),
)


class Order(models.Model):
	cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
	ordered_by = models.CharField(max_length=200)
	shipping_address = models.CharField(max_length=200)
	mobile = models.CharField(max_length=10)
	email = models.EmailField(null=True, blank=True)
	total = models.PositiveIntegerField()
	subtotal = models.PositiveIntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
	payment_method = models.CharField(
		max_length=20, choices=METHOD, default="Cash On Delivery")
	payment_completed = models.BooleanField(
		default=False, null=True, blank=True)
	
	def __str__(self):
		return 'Order' + str(self.id)
	