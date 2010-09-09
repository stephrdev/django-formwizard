from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^testapp/', include('test_project.testapp.urls')),
    (r'^testapp2/', include('test_project.testapp2.urls')),
)
