import unittest
import string

from app import current_app as app
from app.api.helpers.exceptions import UnprocessableEntity
from tests.unittests.utils import OpenEventTestCase
from app.api.helpers.utilities import dasherize, require_relationship, string_empty, str_generator
from tests.unittests.setup_database import Setup


class TestUtilitiesHelperValidation(OpenEventTestCase):
    def setUp(self):
        self.app = Setup.create_app()

    def test_dasherize(self):
        """Method to test whether an attribute dasherizes or not"""

        with app.test_request_context():
            field = "starts_at"
            dasherized_field = "starts-at"
            result = dasherize(field)
            self.assertEqual(result, dasherized_field)

    def test_require_relationship(self):
        """Method to test relationship in request data"""

        with self.assertRaises(UnprocessableEntity):
            data = ['event']
            require_relationship(['sponsor', 'event'], data)

    def test_string_empty(self):
        """Method to test whether an empty string is correctly identified."""

        with app.test_request_context():
            self.assertTrue(string_empty(''))
            self.assertTrue(string_empty(' '))
            self.assertFalse(string_empty('some value'))
            self.assertFalse(string_empty('  some   value '))
            self.assertFalse(string_empty(str))
            self.assertFalse(string_empty(int))
            self.assertFalse(string_empty(None))

    def test_str_generator(self):
        """Method to test str_generator."""

        with app.test_request_context():
            generated_string = str_generator()
            self.assertEqual(len(generated_string), 6)
            self.assertRegex(generated_string, r'^[A-Z0-9]+$')
            self.assertNotRegex(generated_string, r'^[a-z]+$')

            generated_string = str_generator(8, chars=string.ascii_lowercase)
            self.assertEqual(len(generated_string), 8)
            self.assertRegex(generated_string, r'^[a-z]+$')
            self.assertNotRegex(generated_string, r'^[A-Z0-9]+$')

            generated_string = str_generator(chars='ABC253')
            self.assertRegex(generated_string, r'^[ABC253]+$')


if __name__ == '__main__':
    unittest.main()
