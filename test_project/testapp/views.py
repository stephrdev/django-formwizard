from django.shortcuts import render_to_response
from django.template import RequestContext

from formwizard.views import SessionWizardView

from testapp.forms import FeedbackStep1, FeedbackStep2, FeedbackStep3


class FeedbackWizard(SessionWizardView):
    template_name = 'testapp/form.html'

    def done(self, form_list, *args, **kwargs):
        return render_to_response(
            'testapp/done.html',
            {'form_list': [form.cleaned_data for form in form_list]},
            context_instance=RequestContext(self.request)
        )

feedback_wizard = FeedbackWizard.as_view(
    [FeedbackStep1, FeedbackStep2, FeedbackStep3])
