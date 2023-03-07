from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, View, CreateView, FormView, DetailView, ListView

from .forms import *
from .models import *
from .utils import password_reset_token


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


def activate(request, uidb64, token):
	User = get_user_model()
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except:
		user = None
	if user is not None and password_reset_token.check_token(user, token):
		user.is_active = True
		user.save()
		messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
		return redirect('ecomm:customerlogin')
	else:
		messages.error(request, "Activation link is invalid!")
	return redirect('ecomm:customerregistration')


def activateEmail(request, user, to_email):
	mail_subject = "Activate your user account."
	message = render_to_string("template_activate_account.html", {
		'user': user.username,
		'domain': get_current_site(request).domain,
		'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		'token': password_reset_token.make_token(user),
		"protocol": 'https' if request.is_secure() else 'http'
	})
	email = EmailMessage(mail_subject, message, to=[to_email])
	try:
		sent = email.send(fail_silently=False)
		if sent:
			messages.success(request, f'Dear {user}, please go to you email {to_email} inbox and click on \
                    received activation link to confirm and complete the registration. \n Note: Check your spam folder.')
		else:
			messages.warning(request, f'Email was not sent to {to_email}')
	except Exception as e:
		messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')
	return None


class CustomerRegistrationView(EcomMixin, CreateView):
	template_name = "customerregistration.html"
	form_class = CustomerRegistrationForm
	success_url = reverse_lazy("ecomm:customerregistration")
	
	def form_valid(self, form):
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		email = form.cleaned_data.get("email")
		user = User.objects.create_user(username, email, password, is_active=False)
		form.instance.user = user
		try:
			activateEmail(self.request, user, email)
			messages.success(self.request, "Activation email sent successfully.")
		except Exception as e:
			messages.error(self.request, f"Failed to send activation email: {str(e)}")
		return super().form_valid(form)


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


class SearchView(EcomMixin, TemplateView):
	template_name = 'search.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		searched_products = Product.objects.all()
		kw = self.request.GET.get('search')
		if kw:
			searched_products = Product.objects.filter(Q(title__icontains=kw) | Q(description__icontains=kw)).order_by(
				'title')
		paginator = Paginator(searched_products, 8)
		page = self.request.GET.get('page')
		try:
			results = paginator.page(page)
		except PageNotAnInteger:
			results = paginator.page(1)
		except EmptyPage:
			results = paginator.page(paginator.num_pages)
		context['results'] = results
		context['search_query'] = kw
		if kw:
			context['search_query'] = kw
			context['search_url'] = f'?search={kw}&'
		return context


# def searches(request):
# 	word = Product.objects.all()
# 	res = request.GET.get('search')
# 	if res:
# 		word = Product.objects.filter(Q(title__icontains=res) | Q(description__icontains=res)).distinct()
# 	paginator = Paginator(word, 8)
# 	page = request.GET.get('page')
# 	try:
# 		results = paginator.page(page)
# 	except PageNotAnInteger:
# 		results = paginator.page(1)
# 	except EmptyPage:
# 		results = paginator.page(paginator.num_pages)
# 	context = {'results': results, 'search_query': res}
# 	if res:
# 		context['search_query'] = res
# 		context['search_url'] = f'?search={res}&'
# 	return render(request, 'search.html', context)


class PasswordForgotView(FormView):
	template_name = "forgotpassword.html"
	form_class = PasswordForgotForm
	success_url = "/forgot-password/?m=s"
	
	def form_valid(self, form):
		email = form.cleaned_data.get("email")
		url = self.request.META['HTTP_HOST']
		customer = Customer.objects.get(user__email=email)
		user = customer.user
		text_content = 'Please Click the link below to reset your password. '
		html_content = url + "/password-reset/" + email + "/" + password_reset_token.make_token(user) + "/"
		send_mail('Password Reset Link | Django Ecommerce', text_content + html_content, settings.EMAIL_HOST_USER,
		          [email], fail_silently=False, )
		return super().form_valid(form)


class PasswordResetView(FormView):
	template_name = "passwordreset.html"
	form_class = PasswordResetForm
	success_url = "/login/"
	
	def dispatch(self, request, *args, **kwargs):
		email = self.kwargs.get("email")
		user = User.objects.get(email=email)
		token = self.kwargs.get("token")
		if user is not None and password_reset_token.check_token(user, token):
			pass
		else:
			return redirect(reverse("ecomm:passworforgot") + "?m=e")
		return super().dispatch(request, *args, **kwargs)
	
	def form_valid(self, form):
		password = form.cleaned_data['new_password']
		email = self.kwargs.get("email")
		user = User.objects.get(email=email)
		user.set_password(password)
		user.save()
		return super().form_valid(form)


"""ADMIN PANEL"""


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
			return redirect("/admin-login/")
		return super().dispatch(request, *args, **kwargs)


class AdminHomeView(AdminRequiredMixin, TemplateView):
	template_name = 'adminpages/adminhome.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["pendingorders"] = Order.objects.filter(order_status="Order Received").order_by("-id")
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


class AdminProductListView(AdminRequiredMixin, ListView):
	template_name = "adminpages/adminproductlist.html"
	queryset = Product.objects.all().order_by("-id")
	context_object_name = "allproducts"


class AdminProductCreateView(AdminRequiredMixin, CreateView):
	template_name = "adminpages/adminproductcreate.html"
	form_class = ProductForm
	success_url = reverse_lazy("ecomm:adminproductlist")
