from datetime import date
from django.test import TestCase
from events.models import SchoolEvents


class SchoolEventsModelTest(TestCase):
    def test_str_representation(self):
        event = SchoolEvents(
            name="Event",
            description="fbvhdkhbdkvbdfkjnk",
            dateevents="1999-01-01",
            year=date.today().year,
        )
        self.assertEqual(str(event), "Event")

    def test_default_year(self):
        event = SchoolEvents(
            name="Test Event",
            description="fbvhdkhbdkvbdfkjnk",
            dateevents="1999-01-01",
        )
        self.assertEqual(event.year, date.today().year)

    def test_custom_year(self):
        event = SchoolEvents(
            name="Test Event",
            description="fbvhdkhbdkvbdfkjnk",
            dateevents="1999-01-01",
            year=2023,
        )
        self.assertEqual(event.year, 2023)
