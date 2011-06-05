from django.test import TestCase

from formwizard.storage import (get_storage,
    MissingStorageModule, MissingStorageClass)
from formwizard.storage.base import BaseStorage


class TestLoadStorage(TestCase):
    def test_load_storage(self):
        self.assertEqual(
            type(get_storage('formwizard.storage.base.BaseStorage', 'wizard1')),
            BaseStorage)

    def test_missing_module(self):
        self.assertRaises(MissingStorageModule, get_storage,
            'formwizard.storage.idontexist.IDontExistStorage', 'wizard1')

    def test_missing_class(self):
        self.assertRaises(MissingStorageClass, get_storage,
            'formwizard.storage.base.IDontExistStorage', 'wizard1')
