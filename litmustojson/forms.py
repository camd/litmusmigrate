from django import forms
from models import Product, Branch, Testgroup
from django.forms import ChoiceField, MultipleChoiceField

class HomeForm(forms.Form):

    product = forms.ModelChoiceField(queryset=Product.objects.all().order_by('name'))
    branch = forms.ModelChoiceField(queryset=Branch.objects.all().order_by('name'))
    testgroups = forms.ModelMultipleChoiceField(queryset=Testgroup.objects.all().order_by('name'))

