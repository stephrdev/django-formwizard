from django.test import TestCase
from django import http
from django import forms
from formwizard.forms import FormWizard
from django.conf import settings
from formwizard.storage.session import SessionStorage
from django.utils.importlib import import_module

class DummyRequest(http.HttpRequest):
    def __init__(self, POST=None):
        super(DummyRequest, self).__init__()
        self.method = POST and "POST" or "GET"
        if POST is not None:
            self.POST.update(POST)
        self.session = {}
        self._dont_enforce_csrf_checks = True

def get_request(*args, **kwargs):
    request = DummyRequest(*args, **kwargs)
    engine = import_module(settings.SESSION_ENGINE)
    request.session = engine.SessionStore(None)
    return request

class Step1(forms.Form):
    name = forms.CharField()

class Step2(forms.Form):
    name = forms.CharField()

class Step3(forms.Form):
    data = forms.CharField()

class TestWizard(FormWizard):
    pass

class FormTests(TestCase):
    def test_form_init(self):
        testform = TestWizard('formwizard.storage.session.SessionStorage', [Step1, Step2])
        self.assertEquals(testform.form_list, {u'0': Step1, u'1': Step2})

        testform = TestWizard('formwizard.storage.session.SessionStorage', [('start', Step1), ('step2', Step2)])
        self.assertEquals(testform.form_list, {u'start': Step1, u'step2': Step2})
        
        testform = TestWizard('formwizard.storage.session.SessionStorage', [Step1, Step2, ('finish', Step3)])
        self.assertEquals(testform.form_list, {u'0': Step1, u'1': Step2, u'finish': Step3})

    def test_first_step(self):
        request = get_request()

        testform = TestWizard('formwizard.storage.session.SessionStorage', [Step1, Step2])
        response = testform(request)
        self.assertEquals(testform.determine_step(), u'0')

        testform = TestWizard('formwizard.storage.session.SessionStorage', [('start', Step1), ('step2', Step2)])
        response = testform(request)

        self.assertEquals(testform.determine_step(), 'start')

    def test_persistence(self):
        request = get_request({'name': 'data1'})

        testform = TestWizard('formwizard.storage.session.SessionStorage', [('start', Step1), ('step2', Step2)])
        response = testform(request)
        self.assertEquals(testform.determine_step(), 'start')
        testform.storage.set_current_step('step2')

        testform2 = TestWizard('formwizard.storage.session.SessionStorage', [('start', Step1), ('step2', Step2)])
        response = testform2(request)
        self.assertEquals(testform2.determine_step(), 'step2')
