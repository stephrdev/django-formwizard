import re
from django.test import TestCase, Client

class WizardTests(object):
    urls = 'formwizard.tests.wizardtests.urls'

    wizard_step_data = (
        {
            'form1-name': 'Pony',
            'form1-thirsty': '2',
        },
        {
            'form2-address1': '123 Main St',
            'form2-address2': 'Djangoland',
        },
        {
            'form3-random_crap': 'blah blah',
        }
    )

    def setUp(self):
        self.client = Client()

    def test_initial_call(self):
        response = self.client.get(self.wizard_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form_step'], 'form1')
        self.assertEqual(response.context['form_step0'], 0)
        self.assertEqual(response.context['form_last_step'], 'form3')
        self.assertEqual(response.context['form_prev_step'], None)
        self.assertEqual(response.context['form_next_step'], 'form2')
        self.assertEqual(response.context['form_step_count'], 3)

    def test_form_post_error(self):
        response = self.client.post(self.wizard_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form_step'], 'form1')
        self.assertEqual(response.context['form'].errors, {'name': [u'This field is required.']})

    def test_form_post_success(self):
        response = self.client.post(self.wizard_url, self.wizard_step_data[0])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form_step'], 'form2')
        self.assertEqual(response.context['form_step0'], 1)
        self.assertEqual(response.context['form_prev_step'], 'form1')
        self.assertEqual(response.context['form_next_step'], 'form3')

    def test_form_stepback(self):
        response = self.client.get(self.wizard_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form_step'], 'form1')

        response = self.client.post(self.wizard_url, self.wizard_step_data[0])
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form_step'], 'form2')

        response = self.client.post(self.wizard_url, {'form_prev_step': response.context['form_prev_step']})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form_step'], 'form1')

    def test_form_finish(self):
        response = self.client.get(self.wizard_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form_step'], 'form1')

        response = self.client.post(self.wizard_url, self.wizard_step_data[0])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form_step'], 'form2')

        response = self.client.post(self.wizard_url, self.wizard_step_data[1])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form_step'], 'form3')

        response = self.client.post(self.wizard_url, self.wizard_step_data[2])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form_list'], [{'name': u'Pony', 'thirsty': True}, {'address1': u'123 Main St', 'address2': u'Djangoland'}, {'random_crap': u'blah blah'}])

class SessionWizardTests(TestCase, WizardTests):
    wizard_url = '/wiz_session/'

class CookieWizardTests(TestCase, WizardTests):
    wizard_url = '/wiz_cookie/'
