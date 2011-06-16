from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.utils import simplejson as json
from django.utils.hashcompat import sha_constructor

import hmac

from formwizard import storage

sha_hmac = sha_constructor


class CookieStorage(storage.BaseStorage):
    encoder = json.JSONEncoder(separators=(',', ':'))

    def __init__(self, *args, **kwargs):
        super(CookieStorage, self).__init__(*args, **kwargs)
        self.data = self.load_data()
        if self.data is None:
            self.init_data()

    def unsign_cookie_data(self, data):
        if data is None:
            return None

        bits = data.split('$', 1)
        if len(bits) == 2:
            if bits[0] == self.get_cookie_hash(bits[1]):
                return bits[1]

        raise SuspiciousOperation('FormWizard cookie manipulated')

    def load_data(self):
        data = self.request.COOKIES.get(self.prefix, None)
        cookie_data = self.unsign_cookie_data(data)
        if cookie_data is None:
            return None
        return json.loads(cookie_data, cls=json.JSONDecoder)

    def update_response(self, response):
        if self.data:
            response.set_cookie(self.prefix, self.create_cookie_data(self.data))
        else:
            response.delete_cookie(self.prefix)
        return response

    def create_cookie_data(self, data):
        encoded_data = self.encoder.encode(self.data)
        cookie_data = '%s$%s' % (self.get_cookie_hash(encoded_data),
            encoded_data)
        return cookie_data

    def get_cookie_hash(self, data):
        return hmac.new('%s$%s' % (settings.SECRET_KEY, self.prefix),
            data, sha_hmac).hexdigest()
