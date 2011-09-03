from django import forms
from models import Products, Branches, Testgroups
from django.forms import ChoiceField, MultipleChoiceField

class HomeForm(forms.Form):

    product = forms.ModelChoiceField(queryset=Products.objects.all().order_by('name'))
    branch = forms.ModelChoiceField(queryset=Branches.objects.all().order_by('name'))
    testgroups = forms.ModelMultipleChoiceField(queryset=Testgroups.objects.all().order_by('name'))

