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
    root_url = models.URLField(max_length=255, null=True)
    visual_url = models.URLField(max_length=255, null=True)
    queries = models.ForeignKey(Queries, on_delete=models.CASCADE, related_name='instances')
    status = models.CharField(default='Pending', max_length=255)

    def __repr__(self):
        """."""
        return 'Query Instance @ {}'.format(self.root_url)



# {'kind': 'bigquery#job', 'etag': '"WLQb94_1oCOtna_uXzhhuBZlpHw/4JCnTUITqluZh1oAfzPTfhUcPFo"',
#  'id': 'bigquerymgr:job_l5GOjEV4bvWwm5viwF5xeRhUA64',
#   'selfLink': 'https://www.googleapis.com/bigquery/v2/projects/bigquerymgr/jobs/job_l5GOjEV4bvWwm5viwF5xeRhUA64',
#    'jobReference': {'projectId': 'bigquerymgr', 'jobId': 'job_l5GOjEV4bvWwm5viwF5xeRhUA64'},
#     'configuration': {'query': {'query': 'SELECT COUNT(*) FROM publicdata:samples.shakesp'}},
#      'status': {'state': 'DONE', 'errorResult': {'reason': 'notFound', 'message': 'Not found: Table publicdata:samples.shakesp'},
#       'errors': [{'reason': 'notFound', 'message': 'Not found: Table publicdata:samples.shakesp'}]},
#       'statistics': {'creationTime': '1501193770845', 'startTime': '1501193770896', 'endTime': '1501193770896'},
#       'user_email': 'Jamessalamonsen@gmail.com'}