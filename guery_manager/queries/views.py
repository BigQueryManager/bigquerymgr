from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from queries.models import Queries, QueryInstance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect


class CreateNewQuery(LoginRequiredMixin, CreateView):
    template_name = 'queries/builder.html'
    model = Queries
    login_url = reverse_lazy('home')
    fields = [
        "name", "query_text", "schedule"
    ]

    def post(self, request):
        """Form post method."""
        # self.object = self.get_object()
        user = request.user
        data = request.POST
        form_info = request.body.decode('utf-8')
        # b'csrfmiddlewaretoken=xdThXZPYamoDKkh9YO9eZBVokfsGXhe30ctVB7s2gdI8OkrsYJThfd5lS3hXKVYo&query=test&schedule=repeat&start-on=2017-07-11+04%3A20&tuesday=true&thursday=true'
        # if data['username'] and data['email']:
        #     user.username = data['username']
        #     user.email = data['email']
        #     user.first_name = data['first_name']
        #     user.last_name = data['last_name']
        #     user.imagerprofile.age = data['age']
        #     user.imagerprofile.job = data['job']
        #     user.imagerprofile.website = data['website']
        #     user.save()
        #     user.imagerprofile.save()
        #     return HttpResponseRedirect(self.get_success_url())
        # return self.render_to_response(self.get_context_data(**kwargs))


class UpdateQuerySchedule(LoginRequiredMixin, UpdateView):
    template_name = 'queries/updatequery.html'
    model = Queries
    login_url = reverse_lazy('home')
