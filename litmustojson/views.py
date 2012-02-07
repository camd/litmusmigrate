from django.core import serializers
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.simplejson import dumps, loads

import logging

from forms import HomeForm
from models import Product, Branch, Testgroup, Subgroup, Testcase

logger = logging.getLogger('console')

def home(request):
    if request.method == 'POST': # If the form has been submitted...
        form = HomeForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass

            # Process the data in form.cleaned_data
            # ...
            
            product = form.cleaned_data['product']
            branch = form.cleaned_data['branch']
            testgroups = form.cleaned_data['testgroups']
            
            response_data = get_response_json(branch, testgroups)

            

            # Create the HttpResponse object with the appropriate CSV header.
            response = HttpResponse(dumps(response_data), mimetype='application/json')
            response['Content-Disposition'] = 'attachment; filename=%s_litmusoutput.json' % product.name
            logger.error(response)

            return response
    else:
        logger.error('logging the request')
        logger.error(request)
        form = HomeForm() # An unbound form

    branches = Branch.objects.all().order_by('name')
    testgroups = Testgroup.objects.all().order_by('name')

    return render_to_response('home.html',
                              {'form': form,
                               'branches': branches,
                               'testgroups': testgroups
                               },
                              context_instance=RequestContext(request))


def get_response_json(branch, testgroups):
    suites = []
    for suite in testgroups:
        suites.append({
            "name": suite.name,
            "description": None
        })

    cases = []
    response_data = {
        "Suites": suites,
        "Cases": cases
    }
    return response_data