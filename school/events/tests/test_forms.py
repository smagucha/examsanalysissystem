from datetime import date
from django.test import TestCase
from events.models import SchoolEvents
from events.forms import eventsforms


class EventsFormsTest(TestCase):
    def test_eventsforms_valid_data(self):
        # Create valid form data
        form_data = {
            "name": "Test Event",
            "description": "This is a test event",
            "dateevents": date.today(),
        }

        # Create an instance of the form with the valid data
        form = eventsforms(data=form_data)

        # Assert that the form is valid
        self.assertTrue(form.is_valid())

    def test_eventsforms_missing_data(self):
        # Create form data with missing required fields
        form_data = {}

        # Create an instance of the form with the missing data
        form = eventsforms(data=form_data)

        # Assert that the form is not valid
        self.assertFalse(form.is_valid())

    def test_eventsforms_invalid_data(self):
        # Create form data with invalid values
        form_data = {
            "name": "",
            "description": "This is a test event",
            "dateevents": "2023-07-01",  # Invalid date format
        }

        # Create an instance of the form with the invalid data
        form = eventsforms(data=form_data)

        # Assert that the form is not valid
        self.assertFalse(form.is_valid())
