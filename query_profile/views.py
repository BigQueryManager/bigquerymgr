from django.shortcuts import render
from django.views import View
from query_profile.models import QueryProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'query_profile/profile.html'
    model = QueryProfile
    login_url = reverse_lazy('home')

    def get(self, request):
        user = request.user
        return self.render_to_response({'user': user})


# class EditProfileView(LoginRequiredMixin, UpdateView):
#     def get(self, request, *args, **kwargs):
#         return blah