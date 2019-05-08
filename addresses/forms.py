from django import forms


from .models import Address

class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = [
			# 'billing_profile',
			# 'address_type',
			'address_line_1',
			'address_line_2',
			'city',
			'country',
			'state',
			'postal_code'
		]
		widgets = {
            'address_line_1': forms.TextInput(attrs={"class":'form-control', "placeholder":"Address line 1", "style":"border: 1px solid gray !important"}),
            'address_line_2': forms.TextInput(attrs={"class":'form-control', "placeholder":"Address line 2", "style":"border: 1px solid gray !important"}),
            'city': forms.TextInput(attrs={"class":'form-control', "placeholder":"city", "style":"border: 1px solid gray !important"}),
            'country': forms.TextInput(attrs={"class":'form-control', "placeholder":"country", "style":"border: 1px solid gray !important"}),
            'state': forms.TextInput(attrs={"class":'form-control', "placeholder":"state", "style":"border: 1px solid gray !important"}),
            'postal_code': forms.TextInput(attrs={"class":'form-control', "placeholder":"Postal code", "style":"border: 1px solid gray !important"})
        }