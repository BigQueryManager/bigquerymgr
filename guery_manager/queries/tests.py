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
from crontab import CronTab, CronItem

fake = faker.Faker()


class QueryFactory(factory.django.DjangoModelFactory):
    """Factory for creating queries."""

    class Meta:
        """Assign to Queries model."""

        model = Queries

    name = fake.text(30)
    query_text = fake.text(200)
    schedule = fake.text(100)
    last_run = datetime.datetime.now()
    # run_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queries')


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

        queries = (QueryFactory.build() for i in range(10))
        for query in queries:
            query.run_by = self.user
            query.save()

    def test_queries_count(self):
        """Check the correct number of queries in database."""
        queries = Queries.objects.count()
        self.assertEqual(queries, 10)

    def test_queries_attached_to_user(self):
        """Test queries attached to correct user."""
        queries = self.user.queries.count()
        self.assertEqual(queries, 10)


class TestAddQueries(TestCase):
    """Test to verify a query is added to the DB and cron."""

    def setUp(self):
        """Create a user and query model info."""
        user = User(
            username='bill',
            email='bill@bob.com'
        )
        user.save()
        self.user = user
        self.client = Client()
        self.name = 'Name this thing'
        self.project = 'monty-python-123456'
        self.query_text = 'SELECT * FROM public:dumb-data'
        self.run_by = user
        self.last_run = 'Pending'

    def test_user_must_be_logged_in_to_add_query(self):
        """User must be logged in to add queries."""
        response = self.client.get(reverse_lazy('queries:build'))
        self.assertRedirects(response, '/?next=/query/build/')

    def test_get_on_add_query_page(self):
        """Test that we get 200 response code for adding queries."""
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('queries:build'))
        self.assertEqual(response.status_code, 200)

    # def test_user_redirects_after_successful_post(self):
    #     """Test that a successful post redirects to the manager."""
    #     self.client.force_login(self.user)
    #     response = self.client.post(reverse_lazy('queries:build'),
    #                                 {'name': self.name, 'project': self.project, 'query': self.query_text, 'schedule': 'run-once', 'start-on': '2017-07-12 13:50'})
    #     self.assertRedirects(response, '/?next=/query/build/')

    # def test_user_post_creates_cron_item(self):
    #     """The post should create a new cron job."""
    #     self.client.force_login(self.user)
    #     self.client.post(reverse_lazy('queries:build'), {'name': self.name, 'project': self.project, 'query': self.query_text, 'schedule': 'run-once', 'start-on': '2017-05-13 04:15'})
    #     the_cron = CronTab(user=True)
    #     search_cmd = '"{}" "{}" "{}"'.format(self.project, self.query_text, self.user.username)
    #     gen_job = the_cron.find_command(search_cmd)
    #     the_job = next(gen_job)
    #     self.assertTrue(isinstance(the_job, CronItem))
