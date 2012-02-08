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
            
            response_data = get_response_json(product, branch, testgroups)

            

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

"""
Return a JSON object in the following format:
{
    "Suites": [
        {
            "name": "suite name",
            "description": "suite description"
        }
    ],
    "Cases": [
        {
            "title": "case title",
            "description": "case description",
            "tags": ["tag1", "tag2", "tag3"],
            "suites": ["suite1 name", "suite2 name", "suite3 name"],
            "steps": [
                {
                    "action": "action text",
                    "expected": "expected text"
                },
                {
                    "action": "action text",
                    "expected": "expected text"
                }
            ]
        }
    ]
}
"""

def get_response_json(product, branch, testgroups):
    suites = []
    for suite in testgroups:
        suites.append({
            "name": suite.name,
            "description": None
        })

    # get the list of subgroups for the selected testgroups.
    # Litmus' data model works that way.  No direct relation between
    # testcases and testgroups.
    subgroups = Subgroup.objects.filter(
        testgroup__in=testgroups
    ).distinct()

    
    cases = []
    
    litmus_testcases = Testcase.objects.filter(
        product = product,
        branch = branch,
        subgroup__in=subgroups).distinct()
    
    
    for litmus_case in litmus_testcases:
        tags = []
        for tag in litmus_case.subgroup.all():
            tags.append(tag.name)

        cases.append({
            "title": litmus_case.summary,
            "description": litmus_case.details,
            "tags": tags,
            "suites": [x.name for x in testgroups],
            "steps": [
                {
                    "action": litmus_case.steps,
                    "expected": litmus_case.expected_results
                }
            ]
        })
    
    
    response_data = {
        "Suites": suites,
        "Cases": cases
    }
    return response_data
    
    
    
    
    
    
    