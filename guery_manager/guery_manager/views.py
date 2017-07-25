from django.shortcuts import render
from django.views import View


class HomeView(View):
    """Home view callable, for the home page."""
    def get(self, request):
        context = {'user': request.user}
        return render(request, 'guery_manager/home.html', context=context)
