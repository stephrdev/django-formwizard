from django.utils.datastructures import SortedDict
from django.shortcuts import render_to_response
from django.template import RequestContext
from formwizard.storage import get_storage
from django import forms

class FormWizard(object):
    def __init__(self, storage, form_list, initial_list={}, instance_list={}):
        self.form_list = SortedDict()
        self.storage_name = storage

        assert len(form_list) > 0, 'at least one form is needed'

        for i in range(len(form_list)):
            form = form_list[i]
            if isinstance(form, tuple):
                self.form_list[unicode(form[0])] = form[1]
            else:
                self.form_list[unicode(i)] = form

        self.initial_list = initial_list
        self.instance_list = instance_list

    def __repr__(self):
        return 'step: %s, form_list: %s, initial_list: %s' % (
            self.determine_step(), self.form_list, self.initial_list)

    def __call__(self, request, *args, **kwargs):
        self.request = request
        self.storage = get_storage(self.storage_name, self.get_wizard_name(), self.request)
        response = self.process_request(*args, **kwargs)
        response = self.storage.update_response(response)

        return response

    def process_request(self, *args, **kwargs):
        if self.request.method == 'GET':
            return self.process_get_request(*args, **kwargs)
        else:
            return self.process_post_request(*args, **kwargs)

    def process_get_request(self, *args, **kwargs):
        self.reset_wizard()

        if 'extra_context' in kwargs:
            self.update_extra_context(kwargs['extra_context'])

        self.storage.set_current_step(self.get_first_step())
        return self.render(self.get_form())

    def process_post_request(self, *args, **kwargs):
        if 'extra_context' in kwargs:
            self.update_extra_context(kwargs['extra_context'])

        if self.request.POST.has_key('form_prev_step') and self.form_list.has_key(self.request.POST['form_prev_step']):
            self.storage.set_current_step(self.request.POST['form_prev_step'])
            form = self.get_form(data=self.storage.get_step_data(self.determine_step()))
        else:
            form = self.get_form(data=self.request.POST)

            if form.is_valid():
                self.storage.set_step_data(self.determine_step(), self.process_step(form))

                if self.determine_step() == self.get_last_step():
                    return self.render_done(form, *args, **kwargs)
                else:
                    return self.render_next_step(form, *args, **kwargs)
        return self.render(form)

    def render_next_step(self, form, *args, **kwargs):
        next_step = self.get_next_step()
        new_form = self.get_form(next_step, data=self.storage.get_step_data(next_step))
        self.storage.set_current_step(next_step)
        return self.render(new_form)

    def render_done(self, form, *args, **kwargs):
        final_form_list = []
        for form_key in self.form_list.keys():
            form_obj = self.get_form(step=form_key, data=self.storage.get_step_data(form_key))
            if not form_obj.is_valid():
                return self.render_revalidation_failure(form_key, form_obj)
            final_form_list.append(form_obj)
        return self.done(self.request, final_form_list)

    def get_form_prefix(self, step=None, form=None):
        if step is None:
            step = self.determine_step()
        return str(step)

    def get_form_initial(self, step):
        return self.initial_list.get(step, {})

    def get_form_instance(self, step):
        return self.instance_list.get(step, None)

    def get_form(self, step=None, data=None):
        if step is None:
            step = self.determine_step()
        kwargs = {
            'data': data,
            'prefix': self.get_form_prefix(step, self.form_list[step]),
            'initial': self.get_form_initial(step),
        }
        if issubclass(self.form_list[step], forms.ModelForm):
            kwargs.update({'instance': self.get_form_instance(step)})
        return self.form_list[step](**kwargs)

    def process_step(self, form):
        return self.get_form_step_data(form)

    def render_revalidation_failure(self, step, form):
        self.storage.set_current_step(step)
        return self.render(form)

    def get_form_step_data(self, form):
        return form.data

    def get_all_cleaned_data(self):
        cleaned_dict = {}
        for form_key in self.form_list.keys():
            form_obj = self.get_form(step=form_key, data=self.storage.get_step_data(form_key))
            if form_obj.is_valid():
                if isinstance(form_obj.cleaned_data, list):
                    cleaned_dict.update({'formset-%s' % form_key: form_obj.cleaned_data})
                else:
                    cleaned_dict.update(form_obj.cleaned_data)
        return cleaned_dict

    def get_cleaned_data_for_step(self, step):
        if self.form_list.has_key(step):
            form_obj = self.get_form(step=step, data=self.storage.get_step_data(step))
            if form_obj.is_valid():
                return form_obj.cleaned_data
        return None

    def determine_step(self):
        return self.storage.get_current_step() or self.get_first_step()

    def get_first_step(self):
        return self.form_list.keys()[0]

    def get_last_step(self):
        return self.form_list.keys()[-1]

    def get_next_step(self, step=None):
        if step is None:
            step = self.determine_step()
        key = self.form_list.keyOrder.index(step) + 1
        if len(self.form_list.keyOrder) > key:
            return self.form_list.keyOrder[key]
        else:
            return None

    def get_prev_step(self, step=None):
        if step is None:
            step = self.determine_step()
        key = self.form_list.keyOrder.index(step) - 1
        if key < 0:
            return None
        else:
            return self.form_list.keyOrder[key]

    def get_step_index(self, step=None):
        if step is None:
            step = self.determine_step()
        return self.form_list.keyOrder.index(step)

    @property
    def num_steps(self):
        return len(self.form_list)

    def get_wizard_name(self):
        return self.__class__.__name__

    def reset_wizard(self):
        self.storage.reset()

    def get_template(self):
        return 'formwizard/wizard.html'

    def get_extra_context(self):
        return self.storage.get_extra_context_data()

    def update_extra_context(self, new_context):
        context = self.get_extra_context()
        context.update(new_context)
        return self.storage.set_extra_context_data(context)

    def render(self, form):
        return self.render_template(form)

    def render_template(self, form=None):
        form = form or self.get_form()
        return render_to_response(self.get_template(), {
            'extra_context': self.get_extra_context(),
            'form_step': self.determine_step(),
            'form_first_step': self.get_first_step(),
            'form_last_step': self.get_last_step(),
            'form_prev_step': self.get_prev_step(),
            'form_next_step': self.get_next_step(),
            'form_step0': int(self.get_step_index()),
            'form_step1': int(self.get_step_index()) + 1,
            'form_step_count': self.num_steps,
            'form': form,
        }, context_instance=RequestContext(self.request))

    def done(self, request, form_list):
        raise NotImplementedError("Your %s class has not defined a done() method, which is required." % self.__class__.__name__)

class SessionFormWizard(FormWizard):
    def __init__(self, *args, **kwargs):
        super(SessionFormWizard, self).__init__('formwizard.storage.session.SessionStorage', *args, **kwargs)

class CookieFormWizard(FormWizard):
    def __init__(self, *args, **kwargs):
        super(CookieFormWizard, self).__init__('formwizard.storage.cookie.CookieStorage', *args, **kwargs)
