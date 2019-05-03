from django.contrib.auth import authenticate, login , get_user_model
from django.http import HttpResponse ,JsonResponse
from django.shortcuts import render, redirect
from products.models import Product
from carts.models import Cart
from .form import ContactForm
from django.views.generic import ListView


def home_page(request):
	#cart_obj, new_obj = Cart.objects.new_or_get(self.request)
	queryset = Product.objects.all()
	product_sale = Product.objects.filter(product_status='sale').first()
	product_before_sale_price = product_sale.price + 10
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	context={
		"title":"Hello World!",
		'object_list': queryset,
		'product_sale':product_sale,
		'product_before_sale_price':product_before_sale_price,
		'cart':cart_obj
	}
	return render(request,"home_page.html",context)


def about_page(request):
	context={
		"title":"About Page"
	}
	return render(request,"home_page.html",context)

def contact_page(request):

	contact_form = ContactForm(request.POST or None)
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	context={
		"title":"Contact Page",
		"form": contact_form,
		"cart": cart_obj
	}
	if contact_form.is_valid():
		if request.is_ajax():
			return JsonResponse({"message":"Thank you for your submission !"})
	if contact_form.errors:
		errors = contact_form.errors.as_json()
		if request.is_ajax():
			return HttpResponse(errors,status=400,content_type='application/json')
	return render(request,"contact/view.html",context)




