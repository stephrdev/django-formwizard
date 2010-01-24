from django.conf.urls.defaults import *
from formwizard.tests.wizardtests.forms import ContactWizard, Page1, Page2, Page3

urlpatterns = patterns('',
    url(r'^wiz/$', ContactWizard([('form1', Page1), ('form2', Page2), ('form3', Page3)])),
    )
