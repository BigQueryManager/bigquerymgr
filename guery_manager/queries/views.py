from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from queries.models import Queries, QueryInstance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect
from crontab import CronTab
import os


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
        new_query.run_by = request.user
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
            days = []
            short_days = []
            if 'sunday' in form_info:
                days.append('Sunday')
                short_days.append('SUN')
            if 'monday' in form_info:
                days.append('Monday')
                short_days.append('MON')
            if 'tuesday' in form_info:
                days.append('Tuesday')
                short_days.append('TUE')
            if 'wednesday' in form_info:
                days.append('Wednesday')
                short_days.append('WED')
            if 'thursday' in form_info:
                days.append('Thursday')
                short_days.append('THU')
            if 'friday' in form_info:
                days.append('Friday')
                short_days.append('FRI')
            if 'saturday' in form_info:
                days.append('Saturday')
                short_days.append('SAT')

            if len(days) == 7:
                day_str = 'day'
            elif len(days) == 7:
                day_str = days[0] + ' and ' + days[1]
            else:
                day_str = ', '.join(days[:-1]) + ', and ' + days[-1]
            new_job.minute.on(int(minute))
            new_job.hour.on(int(hour))
            new_job.dow.on(*short_days)
            new_query.schedule = 'Runs at {}:{} every {}'.format(hour, minute, day_str)
        elif frequency == 'run-once':
            new_job.minute.on(int(minute))
            new_job.hour.on(int(hour))
            new_job.day.on(int(day))
            new_job.month.on(int(month))
            new_query.schedule = 'Run at {}:{} on {}/{}/{}'.format(hour, minute, month, day, year)

        the_cron.write(user=os.getlogin())
        new_query.save()
        return redirect("/")


class UpdateQuerySchedule(LoginRequiredMixin, UpdateView):
    template_name = 'queries/updatequery.html'
    model = Queries
    login_url = reverse_lazy('home')
