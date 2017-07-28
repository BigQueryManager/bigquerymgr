"""Take args from cron job to build BigQuery API call and mutate objects."""

import httplib2
from apiclient import discovery
from oauth2client import client
from django.contrib.auth.models import User
from queries.models import Queries, QueryInstance
import os
import json
from social_django.utils import load_strategy
import datetime


def build_credentials(the_user):
    """Build credentials."""
    extras = the_user.social_auth.values()[0]['extra_data']
    credentials = {
        "access_token": extras['access_token'],
        "client_id": os.environ.get('GOOGLE_KEY'),
        "client_secret": os.environ.get('GOOGLE_SECRET'),
        "refresh_token": extras['refresh_token'],
        "token_expiry": datetime.datetime.fromtimestamp(
            extras['auth_time'] + extras['expires']
        ).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "user_agent": None,
        "revoke_uri": "https://accounts.google.com/o/oauth2/revoke",
        "id_token": None,
        "id_token_jwt": None,
        "token_response": {
            "access_token": extras['access_token'],
            "expires_in": extras['expires'],
            "token_type": "Bearer"
        },
        "scopes": [
            "https://www.googleapis.com/auth/bigquery"
        ],
        "token_info_uri": "https://www.googleapis.com/oauth2/v3/tokeninfo",
        "invalid": False,
        "_class": "OAuth2Credentials",
        "_module": "oauth2client.client"
    }
    return json.dumps(credentials)


def build_instance(project, query_text):
    """Build a query instance."""
    query = Queries.objects.filter(query_text=query_text).filter(project=project)
    query_instance = QueryInstance()
    query_instance.queries = query.first()
    query_instance.save()
    return query_instance


def run(*args):
    """Execute command."""
    try:
        project = args[0]
        query_text = args[1]
        query_instance = build_instance(project, query_text)
        user = args[2]

        user = User.objects.get(username=user)
        social = user.social_auth.get(provider='google-oauth2')
        social.refresh_token(load_strategy())

        credential_inputs = build_credentials(user)
        credentials = client.OAuth2Credentials.from_json(credential_inputs)
        http_auth = credentials.authorize(httplib2.Http())
        bigq = discovery.build('bigquery', 'v2', http=http_auth)

        debug_me = bigq.jobs().insert(
            projectId=project,
            body={
                "kind": "bigquery#job",
                "configuration": {
                    "query": {
                        "query": query_text
                    }
                }
            }
        ).execute()
        # import pdb; pdb.set_trace()
        query = Queries.objects.filter(project=project).filter(query_text=query_text).first()
        if 'errorResult' in debug_me['status']:
            query_instance.status = debug_me['status']['errorResult']['reason']
        else:
            query_instance.status = datetime.datetime.fromtimestamp(
                int(debug_me['statistics']['startTime']) / 1000
            ).strftime('%m-%d-%Y %H:%M')
        query_instance.root_url = debug_me['id']
        query.last_run = datetime.datetime.fromtimestamp(
            int(debug_me['statistics']['startTime']) / 1000
        ).strftime('%m-%d-%Y %H:%M')
        query_instance.save()
        query.save()
        return debug_me
    except IndexError:
        print("Not enough args to run BigQuery script.")
