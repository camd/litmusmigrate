from django import forms
from models import Products, Branches, Testgroups
from django.forms import ChoiceField, MultipleChoiceField

class HomeForm(forms.Form):
    
    product = forms.ModelChoiceField(queryset=Products.objects.all())
    
class ProductDetailForm(forms.Form):

    branch = forms.ModelChoiceField(queryset=Branches.objects.all())
    testgroups = forms.ModelMultipleChoiceField(queryset=Testgroups.objects.all())
    
    def __init__(self, product_id):
        
        product = Products.objects.filter(product_id=product_id)
       # self.branch.queryset = Branches.objects.filter(product=product)        
        #self.testgroups.queryset = Branches.objects.filter(product=product)