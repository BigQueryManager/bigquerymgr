from django.conf.urls import url
from query_profile.views import ProfileView, EditProfileView

app_name = 'query_profile'

urlpatterns = [
    url(r'^$', ProfileView.as_view(), name='profile'),
    # url(r'^edit/$', EditProfileView.as_view(), name='edit_profile'),
]
