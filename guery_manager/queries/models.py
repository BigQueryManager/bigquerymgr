from django.db import models
from django.contrib.auth.models import User


class Queries(models.Model):
    name = models.CharField(max_length=100)
    query_text = models.CharField(max_length=255)
    schedule = models.CharField(max_length=255)
    last_run = models.DateTimeField(null=True, blank=True)
    run_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queries')

    def __repr__(self):
        """."""
        return 'Query: {}'.format(self.name)


class QueryInstance(models.Model):
    root_url = models.URLField(max_length=255)
    visual_url = models.URLField(max_length=255)
    queries = models.ForeignKey(Queries, on_delete=models.CASCADE, related_name='instances')
    status = models.CharField(default='Pending', max_length=16)

    def __repr__(self):
        """."""
        return 'Query Instance @ {}'.format(self.root_url)
