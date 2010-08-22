from django.conf.urls.defaults import *
from test_project.testapp2.forms import feedback_form_instance

urlpatterns = patterns('',
    url(r'^$', feedback_form_instance, name='feedback_wizard2'),
)