
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .models import Review



def review_view(request):
	review_form = ReviewForm(request.POST or None)
	if request.user.is_authenticated():
		context={
			"user": request.user,
			"form": review_form
		}
	if contact_form.is_valid():
		if request.is_ajax():
			return JsonResponse({"message":"Thank you for your review !"})
	if contact_form.errors:
		errors = contact_form.errors.as_json()
		if request.is_ajax():
			return HttpResponse(errors,status=400,content_type='application/json')
	return render(request,"contact/view.html",context)
