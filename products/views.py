# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from analytics.mixins import ObjectViewedMixin
from carts.models import Cart
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator

from .models import Product, ProductView
from .forms import CommentForm


class ProductFeaturedListView(ListView):
	template_name = "products/list.html"

	def get_queryset(self,	*args,	**kwargs):
		request = self.request
		return Product.objects.featured()

class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
	queryset = Product.objects.all().featured()
	template_name = "products/featured-detail.html"

	# def get_queryset(self,	*args,	**kwargs):
	# 	request = self.request
	# 	return Product.objects.featured()

class UserProductHistoryView(LoginRequiredMixin,ListView):
	template_name = "products/user-history.html"
	#template_name = "products/list.html"

	def get_context_data(self, *args,**kwargs):
		context = super(UserProductHistoryView, self).get_context_data(*args,**kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context

	def get_queryset(self,*args,**kwargs):
		request = self.request
		views = request.user.objectviewed_set.by_model(Product,model_queryset=False)#:6
		return views


class ProductListView(ListView):
	# queryset =	Product.objects.all()
	template_name = "products/list.html"

	def get_context_data(self, *args,**kwargs):
		context = super(ProductListView, self).get_context_data(*args,**kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context

	def get_queryset(self,*args,**kwargs):
		request = self.request
		queryset =	Product.objects.all()
		paginator = Paginator(queryset, 3)
		page = request.GET.get('page')
		qs = paginator.page(page)
		return qs


def product_list_view(request):
	queryset =	Product.objects.all()
	p = Paginator(queryset, 4)
	page = request.GET.get('page')
	qs = p.page(page)
	print(qs.count)
	context  = {
		'object_list': qs
	}
	return render(request,"products/list.html",context)



class ProductDetailSlugView(ObjectViewedMixin,DetailView):
	queryset =	Product.objects.all()
	template_name = "products/detail.html"

	def get_context_data(self, *args,**kwargs):
		context = super(ProductDetailSlugView, self).get_context_data(*args,**kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context

	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
		try:
			instance = Product.objects.get(slug=slug, active=True)
		except Product.DoesNotExist:
			raise Http404("Not Found!")
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug=slug,active=True)
			instance = qs.first()
		except:
			raise Http404("OK")
		return instance

class ProductDetailView(ObjectViewedMixin,DetailView):
	#queryset =	Product.objects.all()
	template_name = "products/detail.html"
	form = CommentForm()

	def get_context_data(self,	*args,	**kwargs):
		context = super(ProductDetailView,self).get_context_data(*args,**kwargs)
		print(context)
		context['form'] = self.form
		return context


	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk')
		instance = Product.objects.get_by_id(pk)
		if instance is None:
			raise Http404("Product does not exist")
		return instance

	def product(self, request, *args, **kwargs):
		form = CommentForm(request.POST)
		if form.is_valid():
			product = self.get_object()
			form.instance.user = request.user
			form.instance.product = product
			form.save()
			return redirect(reverse("products", kwargs={
			'pk': product.pk
			}))


def product_detail_view(request, pk=None, *args, **kwargs):
	instance = Product.objects.get_by_id(pk)
	if instance is None:
		raise Http404("Product does not exist")


	form = CommentForm(request.POST or None)
	if request.method == "POST":
		if form.is_valid():
			form.instance.user = request.user
			form.instance.product = instance
			form.save()
			return redirect(reverse("products", kwargs={
			'id': instance.pk
			}))
	context  ={
		'object': instance,
		'form': form
	}
	return render(request,"products/detail.html",context)
