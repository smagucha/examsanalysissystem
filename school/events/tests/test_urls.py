from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from .. import views


class UrlTests(SimpleTestCase):
    def test_addevent_url_resolves(self):
        url = reverse("event:event")
        self.assertEqual(resolve(url).func, views.addevent)

    def test_listevents_url_resolves(self):
        url = reverse("event:listevents")
        self.assertEqual(resolve(url).func, views.listevents)

    def test_updateevent_url_resolves(self):
        url = reverse("event:updateevent", args=[1])
        self.assertEqual(resolve(url).func, views.updateevent)

    def test_delevent_url_resolves(self):
        url = reverse("event:deleteevent", args=[1])
        self.assertEqual(resolve(url).func, views.delevent)
