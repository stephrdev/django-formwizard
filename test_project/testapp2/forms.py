from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response

from formwizard.forms import SessionFormWizard

class FeedbackStep1(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()

class FeedbackStep2(forms.Form):
    support = forms.ChoiceField(choices=(('like', 'like it'), \
        ('dontlike', 'dont like it')))
    performance = forms.ChoiceField(choices=(('like', 'like it'), \
        ('dontlike', 'dont like it')))
    leave_message = forms.BooleanField(required=False)

class FeedbackStep3(forms.Form):
    message = forms.CharField(widget=forms.Textarea())

class FeedbackWizard(SessionFormWizard):
    def done(self, request, storage, form_list):
        return render_to_response(
            'testapp/done.html',
            {'form_list': [form.cleaned_data for form in form_list]},
            context_instance=RequestContext(request)
        )

    def get_template(self, request, storage):
        return ['testapp/form.html',]

feedback_form_instance = FeedbackWizard(
    [FeedbackStep1, FeedbackStep2, FeedbackStep3],
    condition_list={
        '2': lambda w, r, s: (w.get_cleaned_data_for_step(r, s, '1') or {}).get('leave_message', True)
    }
)
