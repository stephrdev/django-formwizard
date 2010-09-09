=========================
Using the NamedFormWizard
=========================

This tutorial is presumes that you have a working FormWizard (as described in the :doc:`gettingstarted` section).

Changing the current FormWizard class
=====================================

To use named urls, you have to subclass `formwizard.forms.NamedUrlFormWizard` instead of `formwizard.forms.FormWizard`.

If you use `formwizard.forms.NamedUrlFormWizard`, you have to define a storage backend manually. To get rid of this, django-formwizard provides two predefined storage backend named url formwizards. NamedUrlSessionFormWizard and NamedUrlCookieFormWizard. The NamedUrlSessionFormWizard will store the step-formdata in a session and the NamedUrlCookieFormWizard will save the formdata in a cookie (which is protected against manipulation).

Create the NamedUrlFormWizard instance
=======================================

To actually use the named url formwizard, we have to create a instance. This can be done once (if you don't need need to add initial data/instance data) or within a view.

.. code-block:: python

    feedback_form_instance = FeedbackWizard([FeedbackStep1, FeedbackStep2, \
        FeedbackStep3], url_name='wiz_feedback')

This differs a bit from the normal FormWizard. You have to add a url_name to define the name of the url which will be used to reverse generate the urls.

After creating the form wizard instance, we need to make the wizard public accessible using a `urls.py`.

.. code-block:: python

    urlpatterns = patterns('',
        url(r'^(?P<step>.+)/$', feedback_form_instance, name='wiz_feedback'),
        url(r'^$', feedback_form_instance, name='wiz_feedback_start'),
    )

To get users to the wizard, you can use the wiz_feedback_start url or get them directly to the first step by using wiz_feedback + step argument.
