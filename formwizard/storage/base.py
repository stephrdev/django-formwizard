class NoFileStorageException(Exception):
    pass

class BaseStorage(object):
    def __init__(self, prefix):
        self.prefix = 'formwizard_%s' % prefix

    def get_current_step(self):
        raise NotImplementedError()

    def set_current_step(self, step):
        raise NotImplementedError()

    def get_step_data(self, step):
        raise NotImplementedError()

    def get_current_step_data(self):
        raise NotImplementedError()

    def set_step_data(self, step, cleaned_data):
        raise NotImplementedError()

    def get_step_files(self, step):
        raise NotImplementedError()

    def set_step_files(self, step, files):
        raise NotImplementedError()

    def get_extra_context_data(self):
        raise NotImplementedError()

    def set_extra_context_data(self, extra_context):
        raise NotImplementedError()

    def reset(self):
        raise NotImplementedError()

    def update_response(self, response):
        raise NotImplementedError()
