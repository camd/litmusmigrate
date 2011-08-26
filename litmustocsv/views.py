from django.shortcuts import render_to_response
from models import Products, Branches, Testgroups
from forms import HomeForm, ProductDetailForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

def home(request):
    if request.method == 'POST': # If the form has been submitted...
        form = HomeForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            product_id = request.POST.get('product')
            
            return HttpResponseRedirect('/litmustocsv/product_detail?product=%s' % product_id) # Redirect after POST
    else:
        form = HomeForm() # An unbound form

    return render_to_response('home.html', 
                              {'form': form,},
                              context_instance=RequestContext(request))

def product_detail(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ProductDetailForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass

            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        product_id = request.GET.get('product')
        form = ProductDetailForm(product_id=product_id) # An unbound form

    return render_to_response('product_detail.html', 
                            {'form': form,},
                            context_instance=RequestContext(request))

                                           

def getcsv(request):
    return render_to_response('csv.html', 
                              {'req': request},
                              context_instance=RequestContext(request))                                          