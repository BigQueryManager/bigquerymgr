from django.db import models
from django.contrib.auth.models import User


class Queries(models.Model):
    name = models.CharField(max_length=100)
    project = models.CharField(max_length=255, null=True)
    query_text = models.CharField(max_length=255)
    schedule = models.CharField(max_length=255)
    last_run = models.CharField(null=True, blank=True, max_length=100)
    run_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queries')

    def __repr__(self):
        """."""
        return 'Query: {}'.format(self.name)


class QueryInstance(models.Model):
    root_url = models.CharField(max_length=255, null=True)
    visual_url = models.URLField(max_length=255, null=True)
    queries = models.ForeignKey(Queries, on_delete=models.CASCADE, related_name='instances')
    status = models.CharField(default='Pending', max_length=255)

    def __repr__(self):
        """."""
        return 'Query Instance @ {}'.format(self.root_url)
