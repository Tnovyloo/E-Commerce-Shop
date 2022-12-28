from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from .views import payments, place_order
from .models import Payment, Product
from accounts.models import Account
import json
# Create your tests here.

class TestUrls(SimpleTestCase):

    def test_payments_url(self):
        url = reverse('payments')
        self.assertEquals(resolve(url).func, payments)

    def test_place_order(self):
        url = reverse('place_order')
        self.assertEquals(resolve(url).func, place_order)


# class TestViews(TestCase):

#     def test_place_order_view(self):
#         url = reverse("place_order")
#         # resp = client.get(url)
#         user = Account.objects.create(username='testuser')
#         user.set_password('123')
#         user.save()
#
#         client = Client()
#         client.login(username='testuser', password='123')
#
#         response = client.get(url)
#         self.assertEqual(response.status_code, 200)
