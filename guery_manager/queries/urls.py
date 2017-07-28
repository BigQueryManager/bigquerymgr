from django.conf.urls import url
from queries.views import CreateNewQuery, UpdateQuerySchedule

app_name = 'queries'

urlpatterns = [
    url(r'^build/$', CreateNewQuery.as_view(), name='build'),
    url(r'^edit/(?P<pk>\d+)/$', UpdateQuerySchedule.as_view(), name='update'),
]
