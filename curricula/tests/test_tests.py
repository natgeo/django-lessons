from django.test import TestCase


class BaseTestCase(TestCase):

    def test_tests(self):
        self.assertEqual(1, 1)
