from useraccounts.models import MyUser
from django.test import TestCase, Client
from django.urls import reverse
from events.models import SchoolEvents
from datetime import date


class AddEventTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("login")
        SchoolEvents.objects.create(
            name="Test Event",
            description="fbvhdkhbdkvbdfkjnk",
            dateevents="1999-01-01",
            year=date.today().year,
        )
        self.addevent_url = reverse("event:event")
        self.user = MyUser.objects.create(email="testuser", password="testpassword")
        self.listevents_url = reverse("event:listevents")
        self.updateevent_url = reverse("event:updateevent", args=[1])
        self.delevent_url = reverse("event:deleteevent", args=[1])

    def test_addevent_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.addevent_url)
        self.assertEqual(response.status_code, 302)

    def test_addevent_unauthenticated_user(self):
        response = self.client.post(self.addevent_url)
        self.assertEqual(response.status_code, 302)
        expected_redirect_url = f"{self.login_url}?next={self.addevent_url}"
        self.assertRedirects(response, expected_redirect_url)

    def test_listevents_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")
        event = SchoolEvents.objects.create(
            name="Test Event",
            description="fbvhdkhbdkvbdfkjnk",
            dateevents="1999-01-01",
            year=date.today().year,
        )
        response = self.client.get(self.listevents_url)
        self.assertEqual(response.status_code, 302)

    def test_listevents_unauthenticated_user(self):
        response = self.client.get(self.listevents_url)
        self.assertEqual(response.status_code, 302)
        expected_redirect_url = f"{self.login_url}?next={self.listevents_url}"
        self.assertRedirects(response, expected_redirect_url)

    def test_updateevent_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.updateevent_url)
        self.assertEqual(response.status_code, 302)

    def test_updateevent_unauthenticated_user(self):
        response = self.client.post(self.updateevent_url)
        self.assertEqual(response.status_code, 302)
        expected_redirect_url = f"{self.login_url}?next={self.updateevent_url}"
        self.assertRedirects(response, expected_redirect_url)

    def test_delevent_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")
        event = SchoolEvents.objects.create(
            name="Test Event",
            description="fbvhdkhbdkvbdfkjnk",
            dateevents="1999-01-01",
            year=date.today().year,
        )
        response = self.client.post(self.delevent_url)
        self.assertEqual(response.status_code, 302)

    def test_delevent_unauthenticated_user(self):
        response = self.client.post(self.delevent_url)
        self.assertEqual(response.status_code, 302)
        expected_redirect_url = f"{self.login_url}?next={self.delevent_url}"
        self.assertRedirects(response, expected_redirect_url)
