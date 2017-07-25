from django.conf.urls import url
from queries.vies import CreateNewQuery, UpdateQuerySchedule

app_name = 'queries'

url_patterns = [
     url(r'^$', CreateNewQuery.as_view(), name='build'),
     url(r'^$', UpdateQuerySchedule.as_view(), name='update'),
]
