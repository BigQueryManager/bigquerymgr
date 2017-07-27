from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from queries.models import Queries, QueryInstance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect
from crontab import CronTab


class CreateNewQuery(LoginRequiredMixin, CreateView):
    template_name = 'queries/builder.html'
    model = Queries
    login_url = reverse_lazy('home')
    fields = [
        "name", "query_text", "schedule"
    ]

    def post(self, request):
        """Form post method."""
        user = request.user

        form_info = request.body.decode('utf-8')
        new_query = Queries()
        new_query.name = form_info.split('name=')[1].split('&')[0]
        new_query.project = form_info.split('project=')[1].split('&')[0]
        new_query.query_text = form_info.split('query=')[1].split('&')[0]
        frequency = form_info.split('schedule=')[1].split('&')[0]
        start_on = form_info.split('start-on=')[1].split('&')[0]
        year = start_on[:4]
        month = start_on[5:7]
        day = start_on[8:10]
        hour = start_on[11:13]
        minute = start_on[16:18]

        cron_cmd = './manage.py runscript run_big_query --script-args "{}" "{}" "{}"'.format(new_query.project, new_query.query_text, user.username)

        the_cron = CronTab()
        new_job = the_cron.new(command=cron_cmd)

        if frequency == 'repeat':
            pass
        elif frequency == 'run-once':
            new_query.schedule = 'Run at {}:{} on {}/{}/{}'.format(hour, minute, month, day, year)

        the_cron.write()
        new_query.save()
        return redirect("/")


class UpdateQuerySchedule(LoginRequiredMixin, UpdateView):
    template_name = 'queries/updatequery.html'
    model = Queries
    login_url = reverse_lazy('home')
