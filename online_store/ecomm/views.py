from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View, CreateView, FormView, DetailView, ListView
from django.urls import reverse_lazy
from .forms import CheckoutForm, CustomerRegistrationForm, CustomerLoginForm
from django.contrib.auth import authenticate, login, logout
from .models import *


class EcomMixin(object):
	def dispatch(self, request, *args, **kwargs):
		cart_id = request.session.get("cart_id")
		if cart_id:
			cart_obj = Cart.objects.get(id=cart_id)
			if request.user.is_authenticated and request.user.customer:
				cart_obj.customer = request.user.customer
				cart_obj.save()
		return super().dispatch(request, *args, **kwargs)


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


class AddToCartView(EcomMixin, TemplateView):
	template_name = "home.html"

	def get(self, request, *args, **kwargs):
		product_id = self.kwargs['pro_id']
		product_obj = Product.objects.get(id=product_id)
		cart_id = self.request.session.get("cart_id", None)
		if cart_id:
			cart_obj = Cart.objects.get(id=cart_id)
			this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
			if this_product_in_cart.exists():
				cartproduct = this_product_in_cart.last()
				cartproduct.quantity += 1
				cartproduct.subtotal += product_obj.price
				cartproduct.save()
				cart_obj.total += product_obj.price
				cart_obj.save()
				return redirect('ecomm:home')
			else:
				cartproduct = CartProduct.objects.create(
					cart=cart_obj, product=product_obj, rate=product_obj.price, quantity=1, subtotal=product_obj.price)
				cart_obj.total += product_obj.price
				cart_obj.save()
				return redirect('ecomm:home')
		else:
			cart_obj = Cart.objects.create(total=0)
			self.request.session['cart_id'] = cart_obj.id
			cartproduct = CartProduct.objects.create(
				cart=cart_obj, product=product_obj, rate=product_obj.price, quantity=1, subtotal=product_obj.price)
			cart_obj.total += product_obj.price
			cart_obj.save()
		return redirect('ecomm:home')

	
class ManageCartView(View):
	def get(self, request, *args, **kwargs):
		cp_id = self.kwargs["cp_id"]
		action = request.GET.get('action')
		cp_obj = CartProduct.objects.get(id=cp_id)
		cart_obj = cp_obj.cart
		if action == "inc":
			cp_obj.quantity += 1
			cp_obj.subtotal += cp_obj.rate
			cp_obj.save()
			cart_obj.total += cp_obj.rate
			cart_obj.save()
		elif action == "dcr":
			cp_obj.quantity -= 1
			cp_obj.subtotal -= cp_obj.rate
			cp_obj.save()
			cart_obj.total -= cp_obj.rate
			cart_obj.save()
			if cp_obj.quantity == 0:
				cp_obj.delete()
		elif action == "rmv":
			cp_obj.delete()
		else:
			pass
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
	
	
class EmptyCartView(View):
	def get(self, request, *args, **kwargs):
		cart_id = request.session.get("cart_id", None)
		if cart_id:
			cart = Cart.objects.get(id=cart_id)
			cart.cartproduct_set.all().delete()
			cart.total = 0
			cart.save()
		return redirect("ecomm:mycart")
	
	
class CheckoutView(CreateView):
	template_name = "checkout.html"
	form_class = CheckoutForm
	success_url = reverse_lazy('ecomm:home')
	
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated and request.user.customer:
			pass
		else:
			return redirect('/login/?next=checkout/')
		return super().dispatch(request, *args, **kwargs)
		
	def get_context_data(self, **kwargs):
		context = super(CheckoutView, self).get_context_data(**kwargs)
		cart_id = self.request.session.get('cart_id', None)
		if cart_id:
			cart_obj = Cart.objects.get(id=cart_id)
		else:
			cart_obj = None
		context['cart'] = cart_obj
		return context
	
	def form_valid(self, form):
		cart_id = self.request.session.get('cart_id')
		if cart_id:
			cart_obj = Cart.objects.get(id=cart_id)
			form.instance.cart = cart_obj
			form.instance.subtotal = cart_obj.total
			form.instance.total = cart_obj.total
			del self.request.session['cart_id']
		else:
			return redirect('ecomm:home')
		return super().form_valid(form)
	
	
class CustomerRegistrationView(CreateView):
	template_name = "customerregistration.html"
	form_class = CustomerRegistrationForm
	success_url = reverse_lazy("ecomm:home")

	def form_valid(self, form):
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		email = form.cleaned_data.get("email")
		user = User.objects.create_user(username, email, password)
		form.instance.user = user
		login(self.request, user)
		return super().form_valid(form)

	def get_success_url(self):
		if "next" in self.request.GET:
			next_url = self.request.GET.get("next")
			return next_url
		else:
			return self.success_url
		
		
class CustomerLogoutView(View):
	def get(self, request):
		logout(request)
		return redirect('ecomm:home')


class CustomerLoginView(FormView):
	template_name = "customerlogin.html"
	form_class = CustomerLoginForm
	success_url = reverse_lazy("ecomm:home")

	def form_valid(self, form):
		uname = form.cleaned_data.get("username")
		pword = form.cleaned_data["password"]
		usr = authenticate(username=uname, password=pword)
		if usr is not None and Customer.objects.filter(user=usr).exists():
			login(self.request, usr)
		else:
			return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
	
		return super().form_valid(form)
	
	def get_success_url(self):
		if "next" in self.request.GET:
			next_url = self.request.GET.get("next")
			return next_url
		else:
			return self.success_url
		
		
class CustomerProfileView(TemplateView):
	template_name = 'cutomerprofile.html'
	
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
			pass
		else:
			return redirect('/login/?next=profile/')
		return super().dispatch(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		customer = self.request.user.customer
		context['customer'] = customer
		orders = Order.objects.filter(cart__customer=customer).order_by('-id')
		context['orders'] = orders
		return context


class CustomerOrderDetailView(DetailView):
	template_name = "customerorderdetail.html"
	model = Order
	context_object_name = "ord_obj"
	
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
			order_id = self.kwargs["pk"]
			order = Order.objects.get(id=order_id)
			if request.user.customer != order.cart.customer:
				return redirect("ecomm:customerprofile")
		else:
			return redirect("/login/?next=/profile/")
		return super().dispatch(request, *args, **kwargs)
	
	
class AdminLoginView(FormView):
	template_name = "adminpages/adminlogin.html"
	form_class = CustomerLoginForm
	success_url = reverse_lazy('ecomm:adminhome')
	
	def form_valid(self, form):
		uname = form.cleaned_data.get("username")
		pword = form.cleaned_data["password"]
		usr = authenticate(username=uname, password=pword)
		if usr is not None and Admin.objects.filter(user=usr).exists():
			login(self.request, usr)
		else:
			return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
		return super().form_valid(form)

	
class AdminRequiredMixin(object):
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
			pass
		else:
			return redirect('/login/?next=profile/')
		return super().dispatch(request, *args, **kwargs)


class AdminHomeView(AdminRequiredMixin, TemplateView):
	template_name = 'adminpages/adminhome.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['orders'] = Order.objects.all().order_by('-created_at')
		return context
	
	
class AdminDetailView(AdminRequiredMixin, DetailView):
	template_name = 'adminpages/adminorderdetail.html'
	model = Order
	context_object_name = 'ord_obj'

	
class AdminOrderListView(AdminRequiredMixin, ListView):
	template_name = "adminpages/adminorderlist.html"
	queryset = Order.objects.all().order_by("-id")
	context_object_name = "allorders"
	