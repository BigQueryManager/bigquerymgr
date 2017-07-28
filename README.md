# BigQueryManager

This app will allow you to make queries to BigQuery. You will be able to store your data that you've quieried and you will be able to make a visual representation out of that data.

## Repo
https://github.com/BigQueryManager/bigquerymgr

## Development Setup
This is how to setup your development enviroment and run the server.

```sh
git clone https://github.com/BigQueryManager/bigquerymgr.git
cd bigquerymgr
python3 -m venv 'virtual enviroment name' (example = ENV)
pip install -r requirements.pip or requirements.txt
./manage.py runserver
navigate web browser to https://localhost:8000

```

## Authors
James Feore
David Lim
Morgan Nomura
James Salamonsen

## Using the application
### Requirements
- a Google account
- a BigQuery account tied to your Google account
- a BigQuery project tied to your BigQuery account; you must have access to this project

### Sign in
Authenticate using your Google account

### Create a query
Navigate to the Create a Query link in the nav bar.
Enter the input fields in the form; you'll need your BigQuery project id and a valid BigQuery query.
Schedule your query to run on a schedule or once at a given time.

### See your query
All scheduled queries are visible in the Query Manager, accessible from the home route or clicking on the BigQueryManager link in the nav bar.

Clicking on a query will reveal any query instances, which represent every time a scheduled query ran. The query instance will contain links to the query results in BigQuery.

### Update your query
If you'd like to change how often your query runs or stop it from running in the future, you can click on the schedule link on the query. You'll be directed to a form which will allow you to make those changes.

### Logging out
ALERT! If you log out, your scheduled queries will be canceled.
