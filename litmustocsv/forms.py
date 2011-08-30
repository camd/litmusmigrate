from django import forms
from models import Products, Branches, Testgroups
from django.forms import ChoiceField, MultipleChoiceField

class HomeForm(forms.Form):

    product = forms.ModelChoiceField(queryset=Products.objects.all())
    branch = forms.ModelChoiceField(queryset=Branches.objects.all())
    testgroups = forms.ModelMultipleChoiceField(queryset=Testgroups.objects.all())

