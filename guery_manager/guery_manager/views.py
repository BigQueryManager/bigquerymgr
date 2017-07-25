from django.views.generic import ListView
from queries.models import Queries


class HomeView(ListView):
    """Home view callable, for the home page."""
    template_name = 'queries/manager.html'
    model = Queries
    context_object_name = 'queries'

    def get_queryset(self):
        return self.request.user.queries.all()
