import time
import uuid
import httplib2
from apiclient import discovery
from oauth2client import client
from google.cloud import bigquery
from django.contrib.auth.models import User
import os
import json
from social_django.utils import load_strategy
#...
# social = request.user.social_auth.get(provider='google-oauth2')
# access_token = social.get_access_token(load_strategy())


the_user = User.objects.first()

build_credentials = {
    "access_token": the_user.social_auth.values()[0]['extra_data']['access_token'],
    "client_id": os.environ.get('GOOGLE_KEY'),
    "client_secret": os.environ.get('GOOGLE_SECRET'),
    "refresh_token": None,
    "token_expiry": "2017-07-27T02:21:19Z",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "user_agent": None,
    "revoke_uri": "https://accounts.google.com/o/oauth2/revoke",
    "id_token": None,
    "id_token_jwt": None,
    "token_response": {
        "access_token": the_user.social_auth.values()[0]['extra_data']['access_token'], 
        "expires_in": 3600,
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

credential_inputs = json.dumps(build_credentials)


def run(*args):
    """Execute command."""
    # project, query, user name
    import pdb; pdb.set_trace()
    print(args)
    # project = *args[0]
    # query = *args[1]
    user = User.objects.get(username=args[2])
    social = user.social_auth.get(provider='google-oauth2')
    access_token = social.get_access_token(load_strategy())
    credentials = client.OAuth2Credentials.from_json(credential_inputs)
    http_auth = credentials.authorize(httplib2.Http())
    bigq = discovery.build('bigquery', 'v2', http=http_auth)

    debug_me = bigq.jobs().insert(
        projectId='querymanager-174719',
        body={
            "kind": "bigquery#job",
            "configuration": {
                "query": {
                    "query": "SELECT COUNT(*) FROM publicdata:samples.shakespeare;"
                }
            }
        }
    ).execute()

    return debug_me



#     parser = argparse.ArgumentParser(
#         description=__doc__,
#         formatter_class=argparse.RawDescriptionHelpFormatter)
#     parser.add_argument('query', help='BigQuery SQL Query.')

#     args = parser.parse_args()

#     async_query(args.query)


# def wait_for_job(job):
#     while True:
#         job.reload()  # Refreshes the state via a GET request.
#         if job.state == 'DONE':
#             if job.error_result:
#                 raise RuntimeError(job.errors)
#             return
#         time.sleep(1)


# def async_query(query):
#     client = bigquery.Client()
#     query_job = client.run_async_query(str(uuid.uuid4()), query)
#     query_job.use_legacy_sql = False
#     query_job.begin()

#     wait_for_job(query_job)

#     rows = query_job.results().fetch_data(max_results=10)
#     for row in rows:
#         print(row)