from django.shortcuts import render
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
	
	