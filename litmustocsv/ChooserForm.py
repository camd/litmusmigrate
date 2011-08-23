from django.forms import ModelForm

class ChooserForm(ModelForm):
    branch = forms.ModelChoiceField(queryset=Branches.objects.all())
    class Meta:
        model = Products