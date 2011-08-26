from django.shortcuts import render_to_response
from models import Products, Branches, Testgroups
from forms import HomeForm, ProductDetailForm
from django.http import HttpResponse
from django.template import RequestContext

def home(request):
    if request.method == 'POST': # If the form has been submitted...
        form = HomeForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
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
        form = ProductDetailForm() # An unbound form

    return render_to_response('product.html', 
                            {'form': form,},
                            context_instance=RequestContext(request))

                                           
def exp(request):
  if request.GET.get('product'):
      product = request.GET.get('product')
  else:
      product = None 

  product_list = Products.objects.all()

  if product:
      filter_prod = Products.objects.get(name=product)

      branch_list = Branches.objects.filter(product=filter_prod)
      testgroup_list = Testgroups.objects.filter(product=filter_prod)
  else:
      branch_list = Branches.objects.all()
      testgroup_list = Testgroups.objects.all()

  return render_to_response('exp.html', 
                            {'product_list': product_list,
                             'branch_list': branch_list,
                             'testgroup_list': testgroup_list,
                             'product': product,
                             },
                            context_instance=RequestContext(request))

def getcsv(request):
    return render_to_response('csv.html', 
                              {'req': request},
                              context_instance=RequestContext(request))                                          