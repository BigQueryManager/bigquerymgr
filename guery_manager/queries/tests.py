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
        """Assign to Queries model."""

        model = Queries

    name = fake.text(30)
    project = fake.text(30)
    query_text = fake.text(200)
    schedule = fake.text(100)
    last_run = fake.text(99)


class QueryInstanceFactory(factory.django.DjangoModelFactory):
    """Factory for creating query instances."""

    class Meta:
        """Assign to Queries model."""

        model = QueryInstance

    root_url = fake.text(30)
    visual_url = fake.text(30)
    status = fake.text(10)


class Views(TestCase):
    """Test views."""

    def setUp(self):
        """Set up for tests."""
        user = User(
            username='morgan',
            email='morgan@morgan.com'
        )
        user.save()
        self.user = user
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

    def test_table_on_home_view_authenticated_user(self):
        """Test table appears on home page for authenticated user."""
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('home'))
        html = BeautifulSoup(response.content, 'html.parser')
        table = html.find('table')
        self.assertTrue(table)

    def test_successful_post_to_build_form(self):
        """This should update the databse."""
        self.client.force_login(self.user)

class Models(TestCase):
    """Test Queries and QueryInstance models."""

    def setUp(self):
        """Set up for tests."""
        user = User(
            username='morgan',
            email='morgan@morgan.com'
        )
        user.save()
        self.user = user
        self.client = Client()

        queries = list((QueryFactory.build() for i in range(10)))
        # import pdb; pdb.set_trace()
        for query in queries:
            query.run_by = self.user
            query.save()

        self.queries = queries
        self.query0 = queries[0]
        query_instances = list((QueryInstanceFactory.build() for i in range(10)))
        for query_instance in query_instances:
            query_instance.queries = self.query0
            query_instance.save()

        self.query_instances = query_instances

    def test_queries_count(self):
        """Check the correct number of queries in database."""
        queries = Queries.objects.count()
        self.assertEqual(queries, 10)

    def test_queries_attached_to_user(self):
        """Test queries attached to correct user."""
        queries = self.user.queries.count()
        self.assertEqual(queries, 10)

    def test_query_instances_attached_to_query(self):
        """Test query instances attached to query."""
        self.assertEqual(self.query0.instances.count(), len(self.query_instances))

    def test_delete_query(self):
        """Tests query is successfully deleted from query list."""
        Queries.objects.first().delete()
        self.assertEqual(Queries.objects.count(), len(self.queries) - 1)

    def test_delete_query_instance(self):
        """Tests query is successfully deleted from query list."""
        Queries.objects.first().delete()
        self.assertEqual(QueryInstance.objects.count(), 0)
