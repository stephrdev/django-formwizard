from django import forms


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
