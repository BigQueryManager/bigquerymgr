from django.views.generic import ListView
from queries.models import Queries


class HomeView(ListView):
    """Home view callable, for the home page."""
    template_name = 'guery_manager/manager.html'
    model = Queries
    context_object_name = 'queries'

    def get_context_data(self):
        if self.request.user.is_anonymous():
            return
        else:
            return {'queries': self.request.user.queries.all()}
