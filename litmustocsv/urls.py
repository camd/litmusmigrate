from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^litmustocsv$', 'litmustocsv.views.home', name='home'),
)
