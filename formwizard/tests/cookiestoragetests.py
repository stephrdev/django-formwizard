from django.test import TestCase
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse

from formwizard.storage.cookie import CookieStorage
from formwizard.tests.storagetests import get_request, TestStorage


class TestCookieStorage(TestStorage, TestCase):
    def get_storage(self):
        return CookieStorage

    def test_manipulated_cookie(self):
        request = get_request()
        storage = self.get_storage()('wizard1', request, None)

        storage.data = {'key1': 'value1'}
        response = HttpResponse()
        storage.update_response(response)

        signed_cookie_data = storage.create_cookie_data(storage.data)
        self.assertEqual(response.cookies[storage.prefix].value,
            signed_cookie_data)

        storage.request.COOKIES[storage.prefix] = signed_cookie_data

        self.assertEqual(storage.load_data(), {'key1': 'value1'})

        storage.request.COOKIES[storage.prefix] = 'i_am_manipulated'
        self.assertRaises(SuspiciousOperation, storage.load_data)

    def test_reset_cookie(self):
        request = get_request()
        storage = self.get_storage()('wizard1', request, None)

        storage.data = {'key1': 'value1'}

        response = HttpResponse()
        storage.update_response(response)

        signed_cookie_data = storage.create_cookie_data(storage.data)
        self.assertEqual(response.cookies[storage.prefix].value,
            signed_cookie_data)

        storage.init_data()
        storage.update_response(response)

        self.assertEqual(
            storage.unsign_cookie_data(response.cookies[storage.prefix].value),
            '{"step_files":{},"step":null,"extra_data":{},"step_data":{}}')
