#sign in / sign out
authentication - test if user is authenticated, valid Google user;
authentication reroute - successful sign-in reroutes to home-page.
successful sign-in - creates a Django user
successful second sign-in - no new user generated
bad sign-in - does not redirect to home-page
sign-out redirect - redirects to sign-in page
sigh-out confirmation - confirm user is signed out
sign-in timeout?

#models
valid query object - stored properly
count of query objects - test if # of query is correct
delete query - removes specific query
count of deleted query - test the new # of query after deleted



#forms create views
missing req'd attributes - query object
scheduled form query - create proper string in DB
valid create form - creates a query object
valid create form - updates cron table

#forms update views
update query - updates cron tab
update query - updates DB
stop query - updates cron tab
stop query - updates DB

#manager views
BS4, checking the HTML tag # w/ valid # of stuff
query entries = query count
query sub-entries = count class / tags of <td>; matches query.query count
compare query last run (date/time) to query last run database (date/time)
check links are correct




#cron

test scheduled query time requested =




#handler
test query is returning proper BQ response - use "mocking"
handler invocation creates new query instance on proper query
handler invocation updates last run time on proper query
good query updates query instance status
bad query updates query instance status
handle errors gracefully


#questions
status of BQ?
use mocking? Create fake response from Google to minimize $
