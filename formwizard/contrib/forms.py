from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from formwizard.forms import SessionFormWizard

class NamedUrlSessionFormWizard(SessionFormWizard):
    done_step_name = 'done'

    def __init__(self, *args, **kwargs):
        assert kwargs.has_key('url_name'), 'url name is needed to resolve correct wizard urls'
        self.url_name = kwargs['url_name']
        del kwargs['url_name']
        if kwargs.has_key('done_step_name'):
            self.done_step_name = kwargs['done_step_name']
            del kwargs['done_step_name']
        super(NamedUrlSessionFormWizard, self).__init__(*args, **kwargs)
        assert not self.form_list.has_key(self.done_step_name), 'step name "%s" is reserved for the "done" view' % self.done_step_name

    def process_get_request(self, request, storage, *args, **kwargs):
        if not kwargs.has_key('step'):
            if request.GET.has_key('reset'):
                self.reset_wizard(request, storage)
                storage.set_current_step(self.get_first_step(request, storage))
            if 'extra_context' in kwargs:
                self.update_extra_context(request, storage,
                    kwargs['extra_context'])
            return HttpResponseRedirect(reverse(self.url_name,
                kwargs={'step': self.determine_step(request, storage)}))
        else:
            if 'extra_context' in kwargs:
                self.update_extra_context(request, storage,
                    kwargs['extra_context'])
            step_url = kwargs.get('step', None)
            if step_url == self.done_step_name:
                return self.render_done(request, storage, 
                    self.get_form(request, storage,
                        step=self.get_last_step(request, storage),
                        data=storage.get_step_data(
                            self.get_last_step(request, storage))
                        files=storage.get_step_files(
                            self.get_last_step(request, storage))), **kwargs)
            if step_url <> self.determine_step(request, storage):
                if self.get_form_list(request, storage).has_key(step_url):
                    storage.set_current_step(step_url)
                    return self.render(request, storage,
                        self.get_form(request, storage,
                            data=storage.get_current_step_data(),
                            files=storage.get_current_step_files(),
                            ), **kwargs)
                else:
                    storage.set_current_step(
                        self.get_first_step(request, storage))
                return HttpResponseRedirect(reverse(self.url_name, kwargs={
                    'step': storage.get_current_step()
                }))
            else:
                return self.render(request, storage,
                    self.get_form(request, storage,
                        data=storage.get_current_step_data(),
                        files=storage.get_current_step_files()),
                        **kwargs)

    def process_post_request(self, request, storage, *args, **kwargs):
        if request.POST.has_key('form_prev_step') and \
            self.get_form_list(request, storage).has_key(request.POST['form_prev_step']):
            storage.set_current_step(request.POST['form_prev_step'])
            return HttpResponseRedirect(reverse(self.url_name, kwargs={
                'step': storage.get_current_step()
            }))
        else:
            return super(NamedUrlSessionFormWizard, self).process_post_request(request, storage, *args, **kwargs)

    def render_next_step(self, request, storage, form, **kwargs):
        next_step = self.get_next_step(request, storage)
        storage.set_current_step(next_step)
        return HttpResponseRedirect(reverse(self.url_name,
            kwargs={'step': next_step}))

    def render_revalidation_failure(self, request, storage, failed_step, form, **kwargs):
        storage.set_current_step(failed_step)
        return HttpResponseRedirect(reverse(self.url_name,
            kwargs={'step': storage.get_current_step()}))

    def render_done(self, request, storage, form, **kwargs):
        step_url = kwargs.get('step', None)
        if step_url <> self.done_step_name:
            return HttpResponseRedirect(reverse(self.url_name,
                kwargs={'step': self.done_step_name}))
        return super(NamedUrlSessionFormWizard, self).render_done(request,
            storage, form, **kwargs)
