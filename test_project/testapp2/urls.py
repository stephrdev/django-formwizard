from django.conf.urls.defaults import *
from testapp2.views import feedback_wizard

urlpatterns = patterns('',
    url(r'^$', feedback_wizard, name='feedback_wizard2'),
)
