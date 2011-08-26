from django import forms
from models import Products, Branches, Testgroups
from django.forms import ChoiceField, MultipleChoiceField

class HomeForm(forms.Form):
    
    product = forms.ModelChoiceField(queryset=Products.objects.all())
    
class ProductDetailForm(forms.Form):

    branch = forms.ModelChoiceField(queryset=Branches.objects.all())
    testgroups = forms.ModelMultipleChoiceField(queryset=Testgroups.objects.all())
    
    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id')
        super(ProductDetailForm, self).__init__(*args, **kwargs)

        self.fields['branch'].queryset = Branches.objects.filter(product=product_id)        
        self.fields['testgroups'].queryset = Testgroups.objects.filter(product=product_id)        
