from django.conf.urls.defaults import *
from test_project.testapp.forms import feedback_form_instance

urlpatterns = patterns('',
    url(r'^$', feedback_form_instance, name='feedback_wizard'),
)