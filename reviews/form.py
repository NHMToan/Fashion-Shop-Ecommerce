from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ReviewForm(forms.Form):
	detail = forms.Textield(
				widget=forms.TextInput(
					attrs={
					"class":'form-control',"placeholder":"Full Name"
					}
					)
				)
	stars = forms.PositiveSmallIntegerField(
				widget=forms.PositiveSmallIntegerField(
					)
				)
	