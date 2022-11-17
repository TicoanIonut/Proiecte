from django.views.generic import TemplateView
from .models import *


class HomeView(TemplateView):
	template_name = 'home.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['products'] = Product.objects.all()
		return context
	
	
class ProductDetailView(TemplateView):
	template_name = 'productdetail.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		url_slug = self.kwargs['slug']
		product = Product.objects.get(slug=url_slug)
		context['product'] = product
		return context
	
	
class AddToCartView(TemplateView):
	template_name = 'home.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['products'] = Product.objects.all()
		product_id = self.kwargs['pro_id']
		product_obj = Product.objects.get(id=product_id)
		cart_id = self.request.session.get('cart_id', None)
		if cart_id:
			cart_obj = Cart.objects.get(id=cart_id)
			this_prod_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
			if this_prod_in_cart.exists():
				cartproduct = this_prod_in_cart.last()
				cartproduct.quantity += 1
				cartproduct.subtotal += product_obj.price
				cartproduct.save()
				cart_obj.total += product_obj.price
				cartproduct.save()
			else:
				cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.price,
				                                         quantity=1, subtotal=product_obj.price)
				cart_obj.total += product_obj.price
				cart_obj.save()
		else:
			cart_obj = Cart.objects.create(total=0)
			self.request.session['cart_id'] = cart_obj.id
			cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.price,
			                                         quantity=1, subtotal=product_obj.price)
			cart_obj.total += product_obj.price
			cart_obj.save()
		return context
	
class MyCartView(TemplateView):
	template_name = 'mycart.html'
	
	
	