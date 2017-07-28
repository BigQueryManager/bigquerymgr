"""Query manager views."""

from django.views.generic import ListView, TemplateView
from queries.models import Queries


class HomeView(ListView):
    """Home view callable, for the home page."""

    template_name = 'guery_manager/manager.html'
    model = Queries

    def get_context_data(self):
        """Get queries from user."""
        context = super(HomeView, self).get_context_data()
        if self.request.user.is_anonymous():
            return
        else:
            context['queries'] = self.request.user.queries.all()
            return context


class DocsView(TemplateView):
    """Docs view callable."""

    template_name = 'guery_manager/docs.html'
