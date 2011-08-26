from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^litmustocsv$', 'litmustocsv.views.home', name='home'),
    url(r'^litmustocsv/product_detail/(?P<product_id>\d+)$', 'litmustocsv.views.product_detail', name='product_detail'),

    # fetch the CSV based on the submitted values
    url(r'^litmustocsv/getcsv$', 'litmustocsv.views.getcsv', name='getcsv'),
)
