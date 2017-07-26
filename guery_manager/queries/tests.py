"""Test query app."""

from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from queries.models import Queries, QueryInstance
from bs4 import BeautifulSoup
import faker
import datetime
import factory
# Create your tests here.

fake = faker.Faker()


class QueryFactory(factory.django.DjangoModelFactory):
    """Factory for creating queries."""

    class Meta:
        """Assign to Photo model."""

        model = Queries

    name = fake.text(30)
    query_text = fake.text(200)
    schedule = fake.text(100)
    last_run = datetime.datetime.now()
    # run_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queries')


class Views(TestCase):
    """Test views."""

    def setUp(self):
        """Set up for tests."""
        self.client = Client()

    def test_login_button_home_route_unauthenticated_user(self):
        """Test login button appears for unauthenticated user."""
        response = self.client.get(reverse_lazy('home'))
        html = BeautifulSoup(response.content, 'html.parser')
        login = html.find(id='login')
        self.assertTrue(login)

    def test_table_not_on_home_view_unauthenticated_user(self):
        """Test table does not appear on home page for unauthenticated user."""
        response = self.client.get(reverse_lazy('home'))
        html = BeautifulSoup(response.content, 'html.parser')
        table = html.find('table')
        self.assertFalse(table)
