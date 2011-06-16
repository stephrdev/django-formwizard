=================
django-formwizard
=================

.. warning::

    The 1.0+ releases are incompatible with all previous releases (<=0.6) of
    django-formwizard!

    If you want to use the old version, please install django-formwizard==0.6
    (version 0.6 is the last version with the old api)


django-formwizard is a reusable app to work with multi-page forms. Besides
normal `Forms`, it  supports `FormSets`, `ModelForms` and `ModelFormSets`.

.. note::

    This app was originally developed as an external library for Django but
    the code made it to Django itself. Beginning with release 1.4 of Django,
    the form-wizard will be available in Django directly
    (`django.contrib.formtools.wizard`).

    This code is a backport of the `django.contrib.formtools.wizard` code!

    Until the 1.4 release, django-formwizard will be maintained to let
    Django 1.3 users work with the new form-wizard.


To install django-formwizard, simply run

.. code-block:: console

    # pip install django-formwizard

The source is available on
`GitHub <http://github.com/stephrdev/django-formwizard>`_.

If you are interested in contributing, just fork the repository on GitHub and
commit your changes. Don't forget to send a pull request.
