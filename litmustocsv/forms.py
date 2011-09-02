from django import forms
from models import Products, Branches, Testgroups
from django.forms import ChoiceField, MultipleChoiceField

class HomeForm(forms.Form):

    product = forms.ModelChoiceField(queryset=Products.objects.all().order_by('name'))

