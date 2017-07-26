import argparse
import time
import uuid

from google.cloud import bigquery


def run():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('query', help='BigQuery SQL Query.')

    args = parser.parse_args()

    async_query(args.query)


def wait_for_job(job):
    while True:
        job.reload()  # Refreshes the state via a GET request.
        if job.state == 'DONE':
            if job.error_result:
                raise RuntimeError(job.errors)
            return
        time.sleep(1)


def async_query(query):
    client = bigquery.Client()
    query_job = client.run_async_query(str(uuid.uuid4()), query)
    query_job.use_legacy_sql = False
    query_job.begin()

    wait_for_job(query_job)

    rows = query_job.results().fetch_data(max_results=10)
    for row in rows:
        print(row)
