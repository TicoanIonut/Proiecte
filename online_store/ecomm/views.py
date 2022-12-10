from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView
from .models import *


class HomeView(TemplateView):
	template_name = 'home.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		cart_id = self.request.session.get("cart_id", None)
		if cart_id:
			cart = Cart.objects.get(id=cart_id)
		else:
			cart = None
		context['cart'] = cart
		context['products'] = Product.objects.all()
		return context
	
	
class ProductDetailView(TemplateView):
	template_name = 'productdetail.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		url_slug = self.kwargs['slug']
		product = Product.objects.get(slug=url_slug)
		cart_id = self.request.session.get("cart_id", None)
		if cart_id:
			cart = Cart.objects.get(id=cart_id)
		else:
			cart = None
		context['cart'] = cart
		context['product'] = product
		return context
	
	
class AddToCartView(TemplateView):
	template_name = 'home.html'
	
	def dispatch(self, request, *args, **kwargs):
		context = super().dispatch(request, **kwargs)
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
				return redirect('ecomm:home')
			else:
				cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, price=product_obj.price,
				                                         quantity=1, subtotal=product_obj.price)
				cart_obj.total += product_obj.price
				cart_obj.save()
				return redirect('ecomm:home')
		else:
			cart_obj = Cart.objects.create(total=0)
			self.request.session['cart_id'] = cart_obj.id
			cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, price=product_obj.price,
			                                         quantity=1, subtotal=product_obj.price)
			cart_obj.total += product_obj.price
			cart_obj.save()
		return super(AddToCartView, self).dispatch(request, *args, **kwargs)


class ManageCartView(View):
	def get(self, request, *args, **kwargs):
		cp_id = self.kwargs["cp_id"]
		action = request.GET.get('action')
		cp_obj = CartProduct.objects.get(id=cp_id)
		cart_obj = cp_obj.cart
		if action == "inc":
			cp_obj.quantity += 1
			cp_obj.subtotal += cp_obj.price
			cp_obj.save()
			cart_obj.total += cp_obj.price
			cart_obj.save()
		elif action == "dcr":
			cp_obj.quantity -= 1
			cp_obj.subtotal -= cp_obj.price
			cp_obj.save()
			cart_obj.total -= cp_obj.price
			cart_obj.save()
			if cp_obj.quantity == 0:
				cp_obj.delete()
		return redirect('ecomm:mycart')

	
class MyCartView(TemplateView):
	template_name = "mycart.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		cart_id = self.request.session.get("cart_id", None)
		if cart_id:
			cart = Cart.objects.get(id=cart_id)
		else:
			cart = None
		context['cart'] = cart
		return context
	
	
	