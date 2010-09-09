import hmac

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.utils.hashcompat import sha_constructor
from django.utils import simplejson as json
from formwizard.storage.base import BaseStorage, NoFileStorageException
from django.core.files.uploadedfile import UploadedFile
from django.core.files import File

sha_hmac = sha_constructor

class CookieStorage(BaseStorage):
    step_cookie_key = 'step'
    step_data_cookie_key = 'step_data'
    step_files_cookie_key = 'step_files'
    extra_context_cookie_key = 'extra_context'

    def __init__(self, prefix, request, file_storage, *args, **kwargs):
        super(CookieStorage, self).__init__(prefix)
        self.file_storage = file_storage
        self.request = request
        self.cookie_data = self.load_cookie_data()
        if self.cookie_data is None:
            self.init_storage()

    def init_storage(self):
        self.cookie_data = {
            self.step_cookie_key: None,
            self.step_data_cookie_key: {},
            self.step_files_cookie_key: {},
            self.extra_context_cookie_key: {},
        }
        return True

    def get_current_step(self):
        return self.cookie_data[self.step_cookie_key]

    def set_current_step(self, step):
        self.cookie_data[self.step_cookie_key] = step
        return True

    def get_step_data(self, step):
        return self.cookie_data[self.step_data_cookie_key].get(step, None)

    def get_current_step_data(self):
        return self.get_step_data(self.get_current_step())

    def set_step_data(self, step, cleaned_data):
        self.cookie_data[self.step_data_cookie_key][step] = cleaned_data
        return True


    def set_step_files(self, step, files):
        if files and not self.file_storage:
            raise NoFileStorageException

        if not self.cookie_data[self.step_files_cookie_key].has_key(step):
            self.cookie_data[self.step_files_cookie_key][step] = {}

        for field, field_file in (files or {}).items():
            tmp_filename = self.file_storage.save(field_file.name, field_file)
            file_dict = {
                'tmp_name': tmp_filename,
                'name': field_file.name,
                'content_type': field_file.content_type,
                'size': field_file.size,
                'charset': field_file.charset
            }
            self.cookie_data[self.step_files_cookie_key][step][field] = file_dict

        return True

    def get_current_step_files(self):
        return self.get_step_files(self.get_current_step())

    def get_step_files(self, step):
        session_files = self.cookie_data[self.step_files_cookie_key].get(step, {})

        if session_files and not self.file_storage:
            raise NoFileStorageException

        files = {}
        for field, field_dict in session_files.items():
            files[field] = UploadedFile(
                file=self.file_storage.open(field_dict['tmp_name']),
                name=field_dict['name'],
                content_type=field_dict['content_type'],
                size=field_dict['size'],
                charset=field_dict['charset'],
            )
        return files or None

    def get_extra_context_data(self):
        return self.cookie_data[self.extra_context_cookie_key] or {}

    def set_extra_context_data(self, extra_context):
        self.cookie_data[self.extra_context_cookie_key] = extra_context
        return True

    def reset(self):
        return self.init_storage()

    def update_response(self, response):
        if len(self.cookie_data) > 0:
            response.set_cookie(self.prefix, self.create_cookie_data(self.cookie_data))
        else:
            response.delete_cookie(self.prefix)
        return response

    def load_cookie_data(self):
        data = self.request.COOKIES.get(self.prefix, None)
        if data is None:
            return None

        bits = data.split('$', 1)
        if len(bits) == 2:
            if bits[0] == self.get_cookie_hash(bits[1]):
                return json.loads(bits[1], cls=json.JSONDecoder)

        raise SuspiciousOperation('FormWizard cookie manipulated')

    def get_cookie_hash(self, data):
        return hmac.new('%s$%s' % (settings.SECRET_KEY, self.prefix), data, sha_hmac).hexdigest()

    def create_cookie_data(self, data):
        encoder = json.JSONEncoder(separators=(',', ':'))
        encoded_data = encoder.encode(data)
        return '%s$%s' % (self.get_cookie_hash(encoded_data), encoded_data)
