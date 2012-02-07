from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import HomeForm
from models import Products, Branches, Testgroups
import csv, codecs, cStringIO
from django.utils.simplejson import dumps, loads
from django.core import serializers

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([unicode(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def home(request):
    if request.method == 'POST': # If the form has been submitted...
        form = HomeForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...

            product = form.cleaned_data['product']
            branch_id = form.cleaned_data['branch'].branch_id
            testgroups = form.cleaned_data['testgroups']
            tg_ids = [str(x.testgroup_id) for x in testgroups]

            cursor = connection.cursor()
            cursor.execute(getsql(product.product_id, branch_id, tg_ids))

            # Create the HttpResponse object with the appropriate CSV header.
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment; filename=%s_litmusoutput.csv' % product.name

            csv_writer = UnicodeWriter(response)
            csv_writer.writerow([i[0] for i in cursor.description]) # write headers
            csv_writer.writerows(cursor)
            del csv_writer # this will close the CSV file

            return response
    else:
        form = HomeForm() # An unbound form

    branches = Branches.objects.all().order_by('name')
    testgroups = Testgroups.objects.all().order_by('name')

    return render_to_response('home.html',
                              {'form': form,
                               'branches': branches,
                               'testgroups': testgroups
                               },
                              context_instance=RequestContext(request))


def getsql(product_id, branch_id, testgroup_ids):

    tg_or_statement = ' or tg.testgroup_id = '.join(testgroup_ids)

    sql = '''
select tc.summary as "Test Case name",
       u.email as "Authored By",
       tc.creation_date as "Creation Date",
       tc.details as "Description",
       tc.regression_bug_id as "Bugs",
  tc.steps as "Actions", tc.expected_results as "Expected Results",
  GROUP_CONCAT(REPLACE(sg.name, ",", "%%%%2C")) as "Tags",
  GROUP_CONCAT(REPLACE(tg.name, ",", "%%%%2C")) as "Suites"
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
