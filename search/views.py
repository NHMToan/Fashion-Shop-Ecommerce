
from products.models import Product
from django.views.generic import ListView
from django.shortcuts import render

class SearchProductView(ListView):
	template_name = "search/view.html"

	def get_context_date(self,*args,**kwargs):
		context = super(SearchProductView,self).get_context_data(*args,**kwargs)
		query = self.request.GET.get('q')
		context['query'] = query
		SearchQuery.objects.create(query=query)
		return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		method_dict = request.GET
		query = method_dict.get('q',None)
		if query is not None:
			return Product.objects.search(query)
		return Product.objects.featured()

	
