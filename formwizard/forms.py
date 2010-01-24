from django.utils.datastructures import SortedDict
from django.shortcuts import render_to_response
from django.template import RequestContext
from formwizard.storage import get_storage
from django.views.decorators.csrf import csrf_protect

class FormWizard(object):
    def __init__(self, storage, form_list, initial_list={}):
        self.form_list = SortedDict()
        self.storage_name = storage

        assert len(form_list) > 0, 'at least one form is needed'

        for i in range(len(form_list)):
            form = form_list[i]
            if isinstance(form, tuple):
                self.form_list[form[0]] = form[1]
            else:
                self.form_list[i] = form

        self.initial_list = initial_list

    def __repr__(self):
        return 'step: %s\nform_list: %s\ninitial_list: %s' % (self.step, self.form_list, self.initial_list)

    @csrf_protect
    def __call__(self, request, *args, **kwargs):
        self.current_request = request
        self.storage = get_storage(self.storage_name, self.get_wizard_name(), request)

        if 'extra_context' in kwargs:
            self.update_extra_context(kwargs['extra_context'])

        if request.method == 'GET':
            self.storage.reset()
            self.storage.set_current_step(self.get_first_step())
            return self.render(self.get_form())
        else:
            if request.POST.has_key('form_prev_step') and self.form_list.has_key(request.POST['form_prev_step']):
                self.storage.set_current_step(request.POST['form_prev_step'])
                form = self.get_form(data=self.storage.get_step_data(self.determine_step()))
            else:
                form = self.get_form(data=request.POST)

                if form.is_valid():
                    self.storage.set_step_data(self.determine_step(), self.process_step(form))

                    if self.determine_step() == self.get_last_step():
                        final_form_list = []
                        for form_key in self.form_list.keys():
                            form_obj = self.get_form(step=form_key, data=self.storage.get_step_data(form_key))
                            if not form_obj.is_valid():
                                return self.render_revalidation_failure(form_key, form_obj)
                            final_form_list.append(form_obj)
                        return self.done(self.current_request, final_form_list)
                    else:
                        next_step = self.get_next_step()
                        new_form = self.get_form(next_step, data=self.storage.get_step_data(next_step))
                        self.storage.set_current_step(next_step)
                        return self.render(new_form)
            return self.render(form)

    def get_form_prefix(self, step=None):
        if step is None:
            step = self.determine_step()
        return str(step)

    def get_form_initial(self, step):
        return self.initial_list.get(step, {})

    def get_form(self, step=None, data=None):
        if step is None:
            step = self.determine_step()
        return self.form_list[step](data=data, prefix=self.get_form_prefix(step), initial=self.get_form_initial(step))

    def process_step(self, form):
        return self.get_form_step_data(form)

    def render_revalidation_failure(self, step, form):
        return self.render(form)

    def get_form_step_data(self, form):
        return dict([(form.add_prefix(i), form.cleaned_data[i]) for i in form.cleaned_data.keys()])

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

    def get_template(self):
        return 'formwizard/wizard.html'

    def get_extra_context(self):
        return self.storage.get_extra_context_data()

    def update_extra_context(self, new_context):
        return self.storage.set_extra_context_data(self.get_extra_context().update(new_context))

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
            'form_step0': self.get_step_index(),
            'form_step_count': self.num_steps,
            'form': form,
        }, context_instance=RequestContext(self.current_request))

    def done(self, request, form_list):
        raise NotImplementedError("Your %s class has not defined a done() method, which is required." % self.__class__.__name__)

class SessionFormWizard(FormWizard):
    def __init__(self, form_list, initial_list={}):
        super(SessionFormWizard, self).__init__('formwizard.storage.session.SessionStorage', form_list, initial_list)
