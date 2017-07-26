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


class UpdateQuerySchedule(LoginRequiredMixin, UpdateView):
    template_name = 'queries/updatequery.html'
    model = Queries
    login_url = reverse_lazy('home')
