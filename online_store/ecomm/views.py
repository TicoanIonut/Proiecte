from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View, CreateView, FormView, DetailView, ListView
from django.urls import reverse_lazy, reverse
from .forms import CheckoutForm, CustomerRegistrationForm, CustomerLoginForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class EcomMixin(object):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		cart_id = self.request.session.get("cart_id")
		if cart_id:
			cart_obj = Cart.objects.get(id=cart_id)
			if self.request.user.is_authenticated and self.request.user.customer:
				cart_obj.customer = self.request.user.customer
				cart_obj.save()
			context['cart'] = cart_obj
		return context


class HomeView(EcomMixin, TemplateView):
	template_name = 'home.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		all_products = Product.objects.all().order_by('-id')
		paginator = Paginator(all_products, 8)
		page_number = self.request.GET.get('page')
		product_list = paginator.get_page(page_number)
		context['product_list'] = product_list
		return context
	
	
class ProductDetailView(EcomMixin, TemplateView):
	template_name = 'productdetail.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		url_slug = self.kwargs['slug']
		product = Product.objects.get(slug=url_slug)
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

	
class MyCartView(EcomMixin, TemplateView):
	template_name = "mycart.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context
	
	
class EmptyCartView(EcomMixin, View):
	def get(self, request, *args, **kwargs):
		cart_id = request.session.get("cart_id", None)
		if cart_id:
			cart = Cart.objects.get(id=cart_id)
			cart.cartproduct_set.all().delete()
			cart.total = 0
			cart.save()
		return redirect("ecomm:mycart")
	
	
class CheckoutView(EcomMixin, CreateView):
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
	
	
class CustomerRegistrationView(EcomMixin, CreateView):
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


class CustomerLoginView(EcomMixin, FormView):
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
		
		
class CustomerProfileView(EcomMixin, TemplateView):
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


class CustomerOrderDetailView(EcomMixin, DetailView):
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
	
	
# class SearchView(EcomMixin, TemplateView):
# 	template_name = 'search.html'
#
# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		kw = self.request.GET.get('search')
# 		searched_products = Product.objects.filter(Q(title__icontains=kw) | Q(description__icontains=kw)).order_by('title')
# 		paginator = Paginator(searched_products, 6)
# 		page_number = self.request.GET.get('page') or 1
# 		results = paginator.get_page(page_number)
# 		context = {'results': results, 'search_query': kw}
# 		if kw:
# 			context['search_query'] = kw
# 			context['search_url'] = f'?search={kw}&'
# 		return context


def searches(request):
	word = Product.objects.all()
	res = request.GET.get('search')
	if res:
		word = Product.objects.filter(Q(title__icontains=res) | Q(description__icontains=res)).distinct()
	paginator = Paginator(word, 6)
	page = request.GET.get('page')
	try:
		results = paginator.page(page)
	except PageNotAnInteger:
		results = paginator.page(1)
	except EmptyPage:
		results = paginator.page(paginator.num_pages)
	context = {'results': results, 'search_query': res}
	if res:
		context['search_query'] = res
		context['search_url'] = f'?search={res}&'
	return render(request, 'search.html', context)

# ADMIN PANEL

	
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
		context["pendingorders"] = Order.objects.filter(
			order_status="Order Received").order_by("-id")
		return context
	
	
class AdminDetailView(AdminRequiredMixin, DetailView):
	template_name = 'adminpages/adminorderdetail.html'
	model = Order
	context_object_name = 'ord_obj'


class AdminOrderDetailView(AdminRequiredMixin, DetailView):
	template_name = "adminpages/adminorderdetail.html"
	model = Order
	context_object_name = "ord_obj"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["allstatus"] = ORDER_STATUS
		return context

	
class AdminOrderListView(AdminRequiredMixin, ListView):
	template_name = "adminpages/adminorderlist.html"
	queryset = Order.objects.all().order_by("-id")
	context_object_name = "allorders"
	
	
class AdminOrderStatusChangeView(AdminRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		order_id = self.kwargs["pk"]
		order_obj = Order.objects.get(id=order_id)
		new_status = request.POST.get("status")
		order_obj.order_status = new_status
		order_obj.save()
		return redirect(reverse_lazy("ecomm:adminorderdetail", kwargs={"pk": order_id}))
	
	