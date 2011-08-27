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

            return HttpResponseRedirect('/litmustocsv/product_detail/%s' % product_id) # Redirect after POST
    else:
        form = HomeForm() # An unbound form

    return render_to_response('home.html',
                              {'form': form,},
                              context_instance=RequestContext(request))

def product_detail(request, product_id):
    if request.method == 'POST': # If the form has been submitted...
        form = ProductDetailForm(request.POST, product_id=product_id) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass

            branch_id = form.cleaned_data['branch'].branch_id
            testgroups = form.cleaned_data['testgroups']
            tg_ids = [str(x.testgroup_id) for x in testgroups]

            return render_to_response('sql.html',
                                      {'form': form,
                                       'sql': getsql(product_id,
                                                     branch_id,
                                                     tg_ids,
                                                     )},
                                      context_instance=RequestContext(request))

            #return HttpResponseRedirect('/litmustocsv/getcsv/') # Redirect after POST
    else:
        form = ProductDetailForm(product_id=product_id) # An unbound form

    return render_to_response('product_detail.html',
                            {'form': form,},
                            context_instance=RequestContext(request))



def getcsv(request):
    return render_to_response('csv.html',
                              {'req': request},
                              context_instance=RequestContext(request))

def getsql(product_id, branch_id, testgroup_ids):

    tg_or_statement = ' or tg.testgroup_id = '.join(testgroup_ids)

    sql = '''
select tc.testcase_id, tc.summary, tc.details, tc.regression_bug_id,
  tc.community_enabled, tc.steps, tc.expected_results, u.email,
  GROUP_CONCAT(REPLACE(sg.name, ",", "%%2C")) as tags,
  GROUP_CONCAT(REPLACE(tg.name, ",", "%%2C")) as suites
from testcases AS tc
left join products as p on p.product_id = tc.product_id
left join branches AS b on b.branch_id = tc.branch_id
left join users AS u on tc.author_id = u.user_id
left join testcase_subgroups AS sg_map on tc.testcase_id = sg_map.testcase_id
left join subgroups AS sg on sg_map.subgroup_id = sg.subgroup_id
left join subgroup_testgroups AS tg_map on sg.subgroup_id = tg_map.subgroup_id
right join testgroups AS tg on tg_map.testgroup_id = tg.testgroup_id
where
  p.product_id = %(product_id)s
     and
  b.branch_id = %(branch_id)s
     and
  (tg.testgroup_id = %(tg_or_statement)s)
and
  tc.enabled = 1

group by tc.testcase_id
;
    ''' % {'product_id': product_id,\
           'branch_id': branch_id, \
           'tg_or_statement': tg_or_statement}

    return sql
    #return request